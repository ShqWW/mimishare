from .variable import *
from .utils import generate_unique_code, get_data_json, get_config_json, calculate_expiration_time, get_current_user
from fastapi import Request, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
import os
import shutil
import json
from aiofiles import open as aio_open



async def upload_page(request: Request):
    config_dict = get_config_json()
    return templates.TemplateResponse("upload.html", {"request": request, "filesize_limit": config_dict['filesize'], "chunksize_limit": config_dict['chunksize']})


async def generate_code(request: Request):
    request_data = await request.json()
    code = generate_unique_code()
    data = get_data_json()
    data[code] = (request_data.get("filename", "unknown"), calculate_expiration_time(int(request_data.get("expiration"))))
    async with aio_open(DATAJSONPATH, mode='w') as jsonfile:
        await jsonfile.write(json.dumps(data))
    return JSONResponse(content={"code": code})
    

async def upload_chunk(file: UploadFile = File(...), code: str = Form(...), index: int = Form(...), total_chunks: int = Form(...)):
    chunk_path = os.path.join(BUFFERPATH, code)
    os.makedirs(chunk_path, exist_ok=True)
    chunk_file = os.path.join(chunk_path, str(index).zfill(5))
    with open(chunk_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return JSONResponse(content={"info": f"文件上传成功"})

async def merge_chunk(request: Request):
    request_data = await request.json()
    code = request_data.get("code", "1234")
    data = get_data_json()
    file_name = data[code][0]
    async with aio_open(DATAJSONPATH, mode='w') as jsonfile:
        await jsonfile.write(json.dumps(data))
    chunk_path = os.path.join(BUFFERPATH, code)
    files = os.listdir(chunk_path)
    files_to_merge = [os.path.join(chunk_path, file) for file in files]
    output_folder = os.path.join(UPLOADPATH, code)
    os.makedirs(output_folder)
    output_file = os.path.join(output_folder, file_name)
    # 自定义排序函数
    def sort_key(path):
        # 通过分割字符串获取数字部分，并转换为整数
        return int(path.split('/')[-1])

    # 使用 sorted() 进行排序
    files_to_merge = sorted(files_to_merge, key=sort_key)
    with open(output_file, 'wb') as outfile:
        for filename in files_to_merge:
            with open(filename, 'rb') as infile:
                shutil.copyfileobj(infile, outfile)
    shutil.rmtree(chunk_path)
    return JSONResponse(content={"info": f"文件上合并成功"})


async def server_share_page(request: Request):
    token = request.cookies.get("access_token")  # 从 Cookies 中获取令牌
    # print("Access token retrieved:", token)
    try:
        user = get_current_user(token)  # 验证令牌
    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    file_list = os.listdir(SHAREPATH)
    options = [{"value": file, "label": file} for file in file_list]
    return templates.TemplateResponse("servershare.html", {"request": request, "options": options})


async def server_share(request: Request):
    request_data = await request.json()
    code = generate_unique_code()
    data = get_data_json()
    filename = request_data.get("filename", "unknown")
    expiration = int(request_data.get("expiration"))
    expiration_time = calculate_expiration_time(expiration)
    data[code] = (filename, expiration_time)
    target_dir = os.path.join(UPLOADPATH, code)
    os.makedirs(target_dir)
    shutil.copy(os.path.join(SHAREPATH, filename), os.path.join(target_dir, filename))
    async with aio_open(DATAJSONPATH, mode='w') as jsonfile:
        await jsonfile.write(json.dumps(data))
    return JSONResponse(content={"code": code})

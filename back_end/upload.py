from .variable import *
from .utils import generate_unique_code, read_upload_dict, read_config_dict, calculate_expiration_time, get_current_user, add_record_by_code, search_record_by_code, get_file_size
from fastapi import Request, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
import os
import shutil



async def upload_page(request: Request):
    config_dict = read_config_dict()
    return templates.TemplateResponse("upload.html", {"request": request, "filesize_limit": config_dict['filesize'], "chunksize_limit": config_dict['chunksize']})

async def generate_code(request: Request):
    request_data = await request.json()
    code = generate_unique_code()
    add_record_by_code(code, request_data.get("filename", "unknown"), calculate_expiration_time(int(read_config_dict()["buffertime"])), True)
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
    expiration = request_data.get("expiration", None)
    file_name, _ = search_record_by_code(code)
    deadline = calculate_expiration_time(int(expiration))
    add_record_by_code(code, file_name, deadline, False)
    chunk_path = os.path.join(BUFFERPATH, code)
    files = os.listdir(chunk_path)
    files_to_merge = [os.path.join(chunk_path, file) for file in files]
    output_folder = os.path.join(UPLOADPATH, code)
    os.makedirs(output_folder)
    output_file = os.path.join(output_folder, file_name)
    def sort_key(path):
        return int(path.split('/')[-1])

    files_to_merge = sorted(files_to_merge, key=sort_key)
    with open(output_file, 'wb') as outfile:
        for filename in files_to_merge:
            with open(filename, 'rb') as infile:
                shutil.copyfileobj(infile, outfile)
    shutil.rmtree(chunk_path)
    file_size = get_file_size(output_file)
    return JSONResponse(content={"info": f"文件上合并成功", "filesize": file_size, "deadline": deadline})


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
    data = read_upload_dict()
    filename = request_data.get("filename", "unknown")
    expiration = int(request_data.get("expiration"))
    deadline = calculate_expiration_time(expiration)
    # data[code] = (filename, expiration_time)
    target_dir = os.path.join(UPLOADPATH, code)
    os.makedirs(target_dir)
    output_file = os.path.join(target_dir, filename)
    shutil.copy(os.path.join(SHAREPATH, filename), output_file)
    # write_upload_dict(data)
    add_record_by_code(code, filename, deadline, False)
    file_size = get_file_size(output_file)
    return JSONResponse(content={"code": code, "filename": filename, "filesize": file_size, "deadline": deadline})

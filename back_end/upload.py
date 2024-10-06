from .variable import *
from .utils import generate_unique_code, get_data_json, get_config_json
from fastapi import Request, Form, File, UploadFile
from fastapi.responses import JSONResponse
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
    data[code] = request_data.get("filename", "unknown")
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
    expiration = request_data.get("expiration", 86400)
    # print(expiration) 
    data = get_data_json()
    file_name = data[code]
    chunk_path = os.path.join(BUFFERPATH, code)
    files = os.listdir(chunk_path)
    files_to_merge = [os.path.join(chunk_path, file) for file in files]
    output_folder = os.path.join(UPLOADPATH, code)
    os.makedirs(output_folder)
    output_file = os.path.join(output_folder, file_name)
    with open(output_file, 'wb') as outfile:
        for filename in files_to_merge:
            with open(filename, 'rb') as infile:
                shutil.copyfileobj(infile, outfile)
    shutil.rmtree(chunk_path)
    return JSONResponse(content={"info": f"文件上合并成功"})
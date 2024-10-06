import os
from fastapi import Request
from .variable import *
from .utils import get_data_json
from fastapi import HTTPException 
from fastapi.responses import FileResponse


async def download_page(request: Request):
    files = os.listdir(UPLOADPATH)
    return templates.TemplateResponse("download.html", {"request": request, "files": files})



async def download_file(code: str):
    # 检查取件码是否存在
    data_dict = get_data_json()

    if code not in data_dict:
        raise HTTPException(status_code=404, detail="取件码错误")
    # 获取文件名
    file_name = data_dict[code]
    # 构建文件路径
    file_path = os.path.join(UPLOADPATH, code, file_name)
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在或已经过期")
    # 返回文件下载响应
    return FileResponse(file_path, filename=file_name)
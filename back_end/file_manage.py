from .utils import read_upload_dict, delete_record_by_code, get_current_user
import os
from fastapi.responses import RedirectResponse
from fastapi import HTTPException, Request
from .variable import *
import shutil 
import json


async def list_files(request: Request):
    token = request.cookies.get("access_token")  # 从 Cookies 中获取令牌
    # print("Access token retrieved:", token)
    try:
        user = get_current_user(token)  # 验证令牌
    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    data_dict = read_upload_dict()
    # files = os.listdir(UPLOADPATH)
    # # 过滤出存在的文件
    # files_with_codes = {code: file for code, file in file_codes.items() if file in files}

    return templates.TemplateResponse("filemanage.html", {"request": request, "files_with_codes": data_dict})


async def delete_files(code: str):
    file_folder = os.path.join(UPLOADPATH, code)
    delete_record_by_code(code)
    if os.path.exists(file_folder):
        shutil.rmtree(file_folder)
        return RedirectResponse(url="/filemanage?message=文件%20已删除", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="文件未找到")
from .utils import get_data_json, get_current_user
import os
from fastapi.responses import RedirectResponse
from fastapi import HTTPException, Request
from .variable import *
from aiofiles import open as aio_open
import shutil 
import json


async def list_files(request: Request):
    token = request.cookies.get("access_token")  # 从 Cookies 中获取令牌
    # print("Access token retrieved:", token)
    try:
        user = get_current_user(token)  # 验证令牌
    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    file_codes = get_data_json()
    files = os.listdir(UPLOADPATH)
    # # 过滤出存在的文件
    # files_with_codes = {code: file for code, file in file_codes.items() if file in files}

    return templates.TemplateResponse("filemanage.html", {"request": request, "files_with_codes": file_codes})


async def delete_files(code: str):
    file_codes = get_data_json()
    file_folder = os.path.join(UPLOADPATH, code)
    del file_codes[code]
    async with aio_open(DATAJSONPATH, mode='w') as jsonfile:
        await jsonfile.write(json.dumps(file_codes))

    if os.path.exists(file_folder):
        shutil.rmtree(file_folder)
        return RedirectResponse(url="/filemanage?message=文件%20已删除", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="文件未找到")
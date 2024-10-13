import os
from fastapi import Request
from .variable import *
from .utils import get_file_size, is_outdate, search_record_by_code
from fastapi import HTTPException 
from fastapi.responses import FileResponse, JSONResponse


async def download_page(request: Request):
    files = os.listdir(UPLOADPATH)
    return templates.TemplateResponse("download.html", {"request": request, "files": files})

async def fetch_file(code: str):
    file_name, file_time = search_record_by_code(code)
    if not file_name:
        raise HTTPException(status_code=404, detail="取件码错误")
    file_path = os.path.join(UPLOADPATH, code, file_name)
    if (not os.path.exists(file_path)) or is_outdate(file_time):
        raise HTTPException(status_code=404, detail="文件不存在或已经过期")
    file_size = get_file_size(file_path)
    return JSONResponse(content={"name": file_name, "filesize": file_size})

async def download_file(code: str):
    file_name, deadline = search_record_by_code(code)
    if (not file_name) or (is_outdate(deadline)):
        raise HTTPException(status_code=404, detail="文件不存在或已经过期")

    file_path = os.path.join(UPLOADPATH, code, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在或已经过期")
    return FileResponse(file_path, filename=file_name)



    
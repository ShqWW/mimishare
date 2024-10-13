from .variable import *
from .utils import read_config_dict, write_config_dict, get_current_user
from fastapi import Request, Form, HTTPException
from fastapi.responses import RedirectResponse




def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


def login(request: Request, password: str = Form(...)):
    json_file = read_config_dict()
    password_true = json_file["password"]
    if password != password_true:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Password Error!"})
    response = RedirectResponse(url="/admin", status_code=303)
    response.set_cookie(key="access_token", value="admin")  # 设置 Cookie
    # print("Cookie set: access_token=admin")  # 调试信息
    return response


def logout(request: Request):
    response = RedirectResponse(url="/login")  # 退出后重定向到登录页面
    response.delete_cookie("access_token")  # 删除 Cookie
    return response


async def set_page(request: Request):
    token = request.cookies.get("access_token")  # 从 Cookies 中获取令牌
    # print("Access token retrieved:", token)
    try:
        user = get_current_user(token)  # 验证令牌
    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    config_dict = read_config_dict()
    return templates.TemplateResponse("dashboard.html", {"request": request, "json_data": config_dict})


async def update_config(filesize: int = Form(...), chunksize: int = Form(...), buffertime: int = Form(...), password: str = Form(...)):
    data = {"filesize": filesize, "chunksize": chunksize, "buffertime":buffertime, "password": password}
    write_config_dict(data)
    return {"message": "JSON file updated successfully"}
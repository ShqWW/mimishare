from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import json
import shutil
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi.responses import FileResponse
import random
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有头部
)
app.mount("/background", StaticFiles(directory="background"), name="static")
app.mount("/css", StaticFiles(directory="css"), name="static")
# 模板目录
templates = Jinja2Templates(directory="templates")
UPLOAD_DIRECTORY = "data"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.get("/background")
def get_background():
    # 返回背景图的 URL
    return JSONResponse(content={"url": "/background/a.jpg"})

@app.get("/upload", response_class=HTMLResponse)
async def index(request: Request):
    aaa = get_json()
    return templates.TemplateResponse("upload.html", {"request": request, "sizeLimitMB": aaa['filesize']})

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), expiration: int = Form(...)):
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(expiration)

    json_file_path = 'data_info/datainfo.json' 
    code = generate_unique_code()
    data = get_code()
    data[code] = file.filename
    async with aio_open(json_file_path, mode='w') as jsonfile:
        await jsonfile.write(json.dumps(data))
    
    return JSONResponse(content={"info": f"文件 '{file.filename}' 上传成功，存储在 '{file_location}'。", "code": code})



def get_json():
    json_file_path = 'config/config.json'
    if not os.path.exists(json_file_path):
        return {}
    with open(json_file_path, "r") as file:
        return json.load(file)


def get_code():
    json_file_path = 'data_info/datainfo.json'
    if not os.path.exists(json_file_path):
        return {}
    with open(json_file_path, "r") as file:
        return json.load(file)
    
# 检查当前用户
def get_current_user(token: str):
    if token != "admin":
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, password: str = Form(...)):
    json_file = get_json()
    password_true = json_file["password"]
    if password != password_true:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    response = RedirectResponse(url="/admin", status_code=303)
    response.set_cookie(key="access_token", value="admin")  # 设置 Cookie
    print("Cookie set: access_token=admin")  # 调试信息
    return response

@app.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url="/login")  # 退出后重定向到登录页面
    response.delete_cookie("access_token")  # 删除 Cookie
    return response

@app.get("/download", response_class=HTMLResponse)
async def list_files(request: Request):
    file_codes = get_code()
    files = os.listdir(UPLOAD_DIRECTORY)
    
    # 过滤出存在的文件
    files_with_codes = {code: file for code, file in file_codes.items() if file in files}

    return templates.TemplateResponse("download.html", {"request": request, "files_with_codes": file_codes})


@app.post("/delete/{code}")
async def delete_file(code: str):
    file_codes = get_code()
    filename = file_codes[code]
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    del file_codes[code]
    json_file_path = 'data_info/datainfo.json' 
    async with aio_open(json_file_path, mode='w') as jsonfile:
        await jsonfile.write(json.dumps(file_codes))


    if os.path.isfile(file_path):
        os.remove(file_path)
        return RedirectResponse(url="/download?message=文件%20已删除", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="文件未找到")
    



# @app.get("/download/{filename}")
# async def download_file(filename: str, request: Request):

#     file_path = f"{UPLOAD_DIRECTORY}/{filename}"
#     if os.path.exists(file_path):
#         return JSONResponse(content={"filename": filename, "status": "File found"})
#     return JSONResponse(content={"error": "文件不存在"}, status_code=404)


@app.get("/", response_class=HTMLResponse)
async def list_files(request: Request):

    files = os.listdir(UPLOAD_DIRECTORY)
    return templates.TemplateResponse("code.html", {"request": request, "files": files})



json_file_path = "config/config.json"
from aiofiles import open as aio_open
@app.get("/admin", response_class=HTMLResponse)
async def read_json(request: Request):
    token = request.cookies.get("access_token")  # 从 Cookies 中获取令牌
    print("Access token retrieved:", token)  # 调试信息
    
    try:
        user = get_current_user(token)  # 验证令牌
    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        async with aio_open(json_file_path, mode='r') as file:
            data = await file.read()
            json_data = json.loads(data)
    except FileNotFoundError:
        json_data = {}
    return templates.TemplateResponse("dashboard.html", {"request": request, "json_data": json_data})

@app.post("/admin")
async def update_json(filesize: int = Form(...), password: str = Form(...)):
    data = {"filesize": filesize, "password": password}
    async with aio_open(json_file_path, mode='w') as file:
        await file.write(json.dumps(data))
    return {"message": "JSON file updated successfully"}



@app.get("/download/{pickup_code}")
async def download_file(pickup_code: str):
    # 检查取件码是否存在
    print('aaaaaaaa')
    pickup_codes = get_code()

    if pickup_code not in pickup_codes:
        raise HTTPException(status_code=404, detail="Invalid pickup code")
    
    # 获取文件名
    file_name = pickup_codes[pickup_code]
    
    # 构建文件路径
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    print(file_path)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # 返回文件下载响应
    return FileResponse(file_path, filename=file_name)



def generate_unique_code():
    existing_codes = get_code()
    while True:
        # 生成随机的四位数字
        new_code = f"{random.randint(0, 9999):04d}"
        # 检查是否与已有取件码重复
        if new_code not in existing_codes:
            return new_code


# 运行应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from back_end.variable import *
from back_end.download import download_page, download_file, fetch_file
from back_end.file_manage import list_files, delete_files
from back_end.page import get_background
from back_end.upload import upload_page, upload_chunk, merge_chunk, generate_code, server_share_page, server_share
from back_end.admin import login_page, login, logout, set_page, update_config
from back_end.utils import clear_buffer, set_interval

os.makedirs(UPLOADPATH, exist_ok=True)
os.makedirs(BUFFERPATH, exist_ok=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],  
    allow_headers=["*"], 
)
# app.mount("/background", StaticFiles(directory="background"), name="static")
app.mount("/wallpaper", StaticFiles(directory="wallpaper"), name="wallpaper")
app.mount("/css", StaticFiles(directory="front_end/css"), name="static")
app.mount("/js", StaticFiles(directory="front_end/js"), name="js")

app.get("/", response_class=HTMLResponse)(download_page)
app.get("/fetchfile/{code}")(fetch_file)
app.get("/download/{code}")(download_file)
app.get("/filemanage", response_class=HTMLResponse)(list_files)
app.post("/delete/{code}")(delete_files)
app.get("/background")(get_background)

app.get("/upload", response_class=HTMLResponse)(upload_page)
app.get("/servershare", response_class=HTMLResponse)(server_share_page)

app.post("/generatecode/")(generate_code)
app.post("/uploadchunk/")(upload_chunk)
app.post("/mergechunk/")(merge_chunk)
app.post("/servershareaction/")(server_share)

app.get("/login", response_class=HTMLResponse)(login_page)
app.post("/login", response_class=HTMLResponse)(login)
app.get("/logout")(logout)
app.get("/admin", response_class=HTMLResponse)(set_page)
app.post("/admin")(update_config)

# 运行应用
if __name__ == "__main__":
    interval_timer = set_interval(clear_buffer, 5)
    uvicorn.run(app, host="0.0.0.0", port=80)
    
import os
import json
import random
from fastapi import HTTPException
from .variable import *
from datetime import datetime, timedelta
import shutil
import threading
import logging
logging.basicConfig(level=logging.INFO)

def get_config_json():
    json_file_path = 'config/config.json'
    if not os.path.exists(json_file_path):
        return {}
    with open(json_file_path, "r") as file:
        return json.load(file)

def get_data_json():
    if not os.path.exists(DATAJSONPATH):
        return {}
    with open(DATAJSONPATH, "r") as file:
        return json.load(file)
    
# 检查当前用户
def get_current_user(token: str):
    if token != "admin":
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token

def generate_unique_code():
    existing_codes = get_data_json()
    while True:
        new_code = f"{random.randint(0, 9999):04d}"
        if new_code not in existing_codes:
            return new_code


def calculate_expiration_time(expiration):
    if expiration==0:
        return "2199-01-01 00:00:00"

    # 获取当前时间
    now = datetime.now()
    
    # 计算过期时间
    expiration_time = now + timedelta(seconds=expiration)
    
    # 格式化过期时间为字符串
    expiration_str = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
    
    return expiration_str

def is_outdate(file_time_str):
    # 当前时间
    current_time = datetime.now()
    file_time = datetime.strptime(file_time_str, "%Y-%m-%d %H:%M:%S")

    # 判断文件是否过期
    if file_time > current_time:
        return False
    else:
        return True


def get_file_size(file_path):
    if os.path.exists(file_path):
        size_in_bytes = os.path.getsize(file_path)  # 获取文件大小（字节）
        
        if size_in_bytes < 1024:
            return f"{size_in_bytes} Bytes"
        elif size_in_bytes < 1024**2:
            size_in_kb = size_in_bytes / 1024
            return f"{size_in_kb:.2f} KB"
        elif size_in_bytes < 1024**3:
            size_in_mb = size_in_bytes / (1024**2)
            return f"{size_in_mb:.2f} MB"
        else:
            size_in_gb = size_in_bytes / (1024**3)
            return f"{size_in_gb:.2f} GB"
    else:
        return "文件不存在"
    

def clear_buffer():
    data_dict = get_data_json()
    code_list = list(data_dict.keys())
    delete_code_list = []
    for code in code_list:
        filetime = data_dict[code][1]
        # 过期就清空字典
        if is_outdate(filetime):
            logging.info(f'Deleting file with code: {code}')
            del data_dict[code]
            delete_code_list.append(code)
    with open(DATAJSONPATH, mode='w') as jsonfile:
        jsonfile.write(json.dumps(data_dict))

    tree_list = os.listdir(BUFFERPATH)
    for subfolder in tree_list:
        buffer_path = os.path.join(BUFFERPATH, subfolder)
        if subfolder in delete_code_list and os.path.exists(buffer_path):  
            shutil.rmtree(buffer_path)

    tree_list = os.listdir(UPLOADPATH)
    for subfolder in tree_list:
        upload_path = os.path.join(UPLOADPATH, subfolder)
        if subfolder in delete_code_list and os.path.exists(upload_path): 
            shutil.rmtree(upload_path)


def set_interval(func, interval):
    def wrapper():
        set_interval(func, interval)  # 再次调用以设置下一次定时器
        func()

    timer = threading.Timer(interval, wrapper)
    timer.start()
    return timer  # 返回定时器对象以便后续操作


    
    


    


import os
import json
import random
from fastapi import HTTPException
from .variable import *
from datetime import datetime, timedelta
import shutil
import threading
import sqlite3
import json
import os


CREATE_CONFIG_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS config (
    KEY TEXT PRIMARY KEY,
    VALUE TEXT
);
'''

CREATE_UPLOAD_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS upload (
    code VARCHAR(4) PRIMARY KEY,
    filename TEXT,
    deadline TEXT,
    buffer BOOLEAN
);
'''



def initialize_db():
    if not os.path.exists(DBPATH):
        with sqlite3.connect(DBPATH) as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_CONFIG_TABLE_SQL)
            cursor.execute(CREATE_UPLOAD_TABLE_SQL)
            for key, value in initial_config.items():
                cursor.execute("INSERT OR REPLACE INTO config (KEY, VALUE) VALUES (?, ?)", (key, value))
            conn.commit()

def list_config_dict():
    config_dict = {}
    with sqlite3.connect(DBPATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT KEY, VALUE FROM config")
        results = cursor.fetchall()
        for key, value in results:
            config_dict[key] = value
    return config_dict

def read_config_dict(key=None):
    with sqlite3.connect(DBPATH) as conn:
        cursor = conn.cursor()
        if key is None:
            return None
        else:
            cursor.execute("SELECT VALUE FROM config WHERE KEY = ?", (key,))
            result = cursor.fetchone()
            return result[0] if result else None

def write_config_dict(key, value):
    with sqlite3.connect(DBPATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO config (KEY, VALUE) VALUES (?, ?)", (key, value))
        conn.commit()

def read_upload_dict():
    result_dict = {}
    with sqlite3.connect(DBPATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT code, filename, deadline FROM upload WHERE buffer = False")
        results = cursor.fetchall()
        for row in results:
            result_dict[row[0]] = (row[1], row[2])
        conn.commit()
    return result_dict

def read_buffer_dict():
    result_dict = {}
    with sqlite3.connect(DBPATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT code, filename, deadline FROM upload WHERE buffer = True")
        results = cursor.fetchall()
        for row in results:
            result_dict[row[0]] = (row[1], row[2])
        conn.commit()
    return result_dict

def search_record_by_code(code):
    with sqlite3.connect(DBPATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT filename, deadline FROM upload WHERE code = ?", (code, ))
        results = cursor.fetchone()
        conn.commit()
    if results:
        return results[0], results[1]
    return None, None

def delete_record_by_code(code):
    with sqlite3.connect(DBPATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM upload WHERE code = ?", (code, ))
        conn.commit()
    
def add_record_by_code(code, filename, deadline, buffer):
    with sqlite3.connect(DBPATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO upload (code, filename, deadline, buffer) VALUES (?,?,?,?)", (code, filename, deadline, buffer))
        conn.commit()

def list_existing_codes():
    with sqlite3.connect(DBPATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT code FROM upload')
        results = cursor.fetchall()
        conn.commit() 
    existing_codes = [row[0] for row in results]
    return existing_codes

# 检查当前用户
def get_current_user(token: str):
    if token != "admin":
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token

def generate_unique_code():
    result = True
    with sqlite3.connect(DBPATH) as conn:
        cursor = conn.cursor()
        while result:
            new_code = f"{random.randint(0, 9999):04d}"
            cursor.execute('SELECT code FROM upload WHERE code = ?', (new_code,))
            result = cursor.fetchone()
        conn.commit()
    return new_code

def calculate_expiration_time(expiration):
    if expiration==0:
        return "2199-01-01 00:00:00"

    now = datetime.now()
    expiration_time = now + timedelta(seconds=expiration)
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

def clear_outdate():
    data_dict = read_upload_dict()
    code_list = list(data_dict.keys())
    delete_code_list = []
    for code in code_list:
        filetime = data_dict[code][1]
        if is_outdate(filetime):
            print(f'Clear file with code: {code}')
            delete_record_by_code(code)
            delete_code_list.append(code)
            code_list.remove(code)

    for subfolder in os.listdir(UPLOADPATH):
        tem_path = os.path.join(UPLOADPATH, subfolder)
        if subfolder in delete_code_list: 
            shutil.rmtree(tem_path)

def clear_buffer():
    data_dict = read_buffer_dict()
    code_list = list(data_dict.keys())
    for code in code_list:
        filetime = data_dict[code][1]
        if is_outdate(filetime):
            print(f'Clear buffer with code: {code}')
            delete_record_by_code(code)
            code_list.remove(code)

    for subfolder in os.listdir(BUFFERPATH):
        tem_path = os.path.join(BUFFERPATH, subfolder)
        if subfolder not in code_list: 
            shutil.rmtree(tem_path)


def set_interval(func, interval):
    def wrapper():
        set_interval(func, interval)  # 再次调用以设置下一次定时器
        func()

    timer = threading.Timer(interval, wrapper)
    timer.start()
    return timer  # 返回定时器对象以便后续操作


    
    


    


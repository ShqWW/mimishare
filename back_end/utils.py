import os
import json
import random
from fastapi import HTTPException
from .variable import *

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
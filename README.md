# MIMI Share 临时文件分享

## 使用说明
后台地址：`{ip}:{port}/admin`

默认密码：admin

### 服务器文件分享：
服务器文件先放在`share`文件夹下，进后台下拉菜单选择需要分享的文件

##部署
### docker打包镜像

运行打包脚本
```
sh pack.sh
```

docker-compose:
```
---
services:
  mimishare:
    image: catwsq/mimishare:latest
    container_name: mimishare
    ports:
      - "80:80"
    volumes:
      - ./data:/app/data
      - ./share:/app/share
      - ./wallpaper:/app/wallpaper
      - ./config:/app/config
    restart: always
```

### python 直接运行

新建目录以及安装package
```
mkdir share
mkdir data
mkdir buffer
pip install -r requirements.txt
```

运行
```
python main.py
```




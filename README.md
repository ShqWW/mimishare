# docker打包镜像

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

# python 直接运行

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




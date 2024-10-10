<div align="center">
    <img src="icon/logo.svg" alt="图标" width="80" height="80" style="vertical-align: middle;"/> 
     <h1 style="display: inline; background: linear-gradient(45deg, #007bff, #00aaff, #b700ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        MIMISHARE
    </h1>
    <h2 style="display: inline; vertical-align: middle;">部署在NAS上的轻量文件分享软件</h2>
</div>


## 界面预览
![demo1](mdpic/pic1.jpg)
![demo2](mdpic/pic2.jpg)

## 使用说明

### 游客使用
分享文件得到取件码，其他人使用取件码可以下载。

### 进入后台
管理员后台地址：`ip:port/admin` 其中`ip`和`port`替换为实际IP和端口值。

默认密码：`admin`

进入后台可以管理文件和设置参数，也可以进行服务器文件分享。
配置文件和文件信息存储在`config`目录下，分享的文件保存在`data`目录下。配置尽量在web端后台操作，尽量不要手动修改文件。

### 服务器文件分享：
服务器文件先放在`share`文件夹下，进后台下拉菜单选择需要分享的文件。

### 壁纸修改：
壁纸放在wallpaper目录下即可，壁纸名称为 `background.jpg`

## 部署
### 方式1 (推荐)--Docker拉取镜像：

直接使用docker-compose拉取镜像：
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
### 方式2--本地打包Docker镜像：
进入项目根目录，运行打包脚本:
```
sh pack.sh
```

### 方式3--python 直接运行

新建目录并安装package：
```
mkdir share
mkdir data
mkdir buffer
pip install -r requirements.txt
```

运行 (需要手动更改`main.py`的端口，默认80)：
```
python main.py
```




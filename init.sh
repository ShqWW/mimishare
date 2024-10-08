#!/bin/bash

if [ ! -f /app/config/config.json ]; then
    cp /container/config/config.json /app/config/config.json
else
    echo "config.json already exists in mounted directory, skipping copy."
fi


if [ ! -f /app/config/datainfo.json ]; then
    cp /container/config/datainfo.json /app/config/datainfo.json
else
    echo "datainfo.json already exists in mounted directory, skipping copy."
fi

if [ ! -f /app/wallpaper/background.jpg ]; then
    cp /container/wallpaper/background.jpg /app/wallpaper/background.jpg
else
    echo "background.jpg already exists in mounted directory, skipping copy."
fi

rm -rf /container

# 继续执行应用的启动命令
exec python main.py
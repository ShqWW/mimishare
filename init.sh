#!/bin/bash
if [ ! -f /app/wallpaper/background.jpg ]; then
    cp /container/wallpaper/background.jpg /app/wallpaper/background.jpg
else
    echo "background.jpg already exists in mounted directory, skipping copy."
fi

# 继续执行应用的启动命令
exec python main.py
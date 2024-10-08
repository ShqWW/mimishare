FROM python:3.9.5-slim-buster

COPY . /app
COPY ./config /container/config
COPY ./wallpaper /container/wallpaper


RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone
WORKDIR /app

RUN mkdir -p /app/buffer
RUN mkdir -p /app/share
RUN mkdir -p /app/data

RUN pip install -r requirements.txt
EXPOSE 80
RUN chmod +x /app/init.sh
RUN rm -rf /app/Dockerfile /app/pack.sh /app/requirements.txt
CMD ["/app/init.sh"]
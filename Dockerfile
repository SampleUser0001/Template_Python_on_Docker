# 任意のイメージを取得
FROM python:3.10-rc-slim-buster

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

WORKDIR /opt/app

COPY app /opt/app

RUN chmod 755 /opt/app/start.sh

RUN python --version

CMD [ "/opt/app/start.sh" ]

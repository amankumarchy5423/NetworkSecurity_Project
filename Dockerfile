FROM python:3.10-slim-buster

WORKDIR /app

COPY ./app

RUN apt update -y && apt install awscli -y

CMD ["python3","app.py"]
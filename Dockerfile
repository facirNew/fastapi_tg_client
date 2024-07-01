FROM python:3.11.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY requirements.txt /app/requirements.txt

RUN ["pip", "install", "-r", "app/requirements.txt"]

COPY /app /app

WORKDIR /app

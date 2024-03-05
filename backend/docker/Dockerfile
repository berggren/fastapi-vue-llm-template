# pull official base image
FROM python:3.11.3-slim-buster

# set working directory
WORKDIR /fastapi

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt


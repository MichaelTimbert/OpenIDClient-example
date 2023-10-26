FROM python:3.11-slim-bullseye

WORKDIR /usr/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# update pip
RUN pip install --upgrade pip

COPY ./ /usr/app
RUN pip install --no-cache-dir --upgrade -r requirement.txt

CMD uvicorn main:app --host 0.0.0.0 


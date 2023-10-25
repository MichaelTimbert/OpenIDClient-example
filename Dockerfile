FROM python:3.11-slim-bullseye

WORKDIR /usr/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# update pip
RUN pip install --upgrade pip

COPY ./ /usr/app
RUN pip install --no-cache-dir --upgrade -r requirement.txt

# --forwarded-allow-ip is needed to have the real ip client in log otherwise we have the ip of treafik
#CMD python3 -m uvicorn beekey.server:app --proxy-headers --forwarded-allow-ips '*' --host 0.0.0.0 --port 80
CMD uvicorn main:app --host 0.0.0.0 


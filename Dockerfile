# FROM alpine:latest

# RUN apk add --no-cache python3-dev \
#     && python3 -m ensurepip \
#     && pip3 install --upgrade pip

# WORKDIR /app

# COPY . /app

# RUN pip3 --no-cache-dir install -r requirements.txt

# EXPOSE 5000

# CMD ["python3", "app.py"]

FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get install -y python3-pip

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]

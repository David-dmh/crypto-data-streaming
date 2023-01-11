FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get install -y python3-pip

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

ENV SECRET_KEY=fdkjshfhjsdfdskfdsfdcbsjdkfdsdf
ENV DEBUG=True
ENV APP_SETTINGS=config.DevelopmentConfig
ENV DATABASE_URL=sqlite:///db.sqlite
ENV SQLALCHEMY_TRACK_MODIFICATIONS=False
ENV FLASK_APP=src
ENV FLASK_DEBUG=1

EXPOSE 5000

RUN cd src && python3 __init__.py
RUN cd .. && python3 manage.py


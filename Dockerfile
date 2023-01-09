FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get install -y python3-pip

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

CMD ["python3", "src/__init__.py"]
# CMD ["python3", "app.py"]

# RUN ".env"

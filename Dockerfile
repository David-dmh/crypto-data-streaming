FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get install -y python3-pip

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

# RUN cd src 
# CMD ["python3", "__init__.py"]
RUN cd src && python3 __init__.py

# RUN rm /bin/sh && ln -s /bin/bash /bin/sh
# RUN source .env

# CMD ["python3", "__init__.py"]

# CMD ["python3", "app.py"]

# RUN ".env"

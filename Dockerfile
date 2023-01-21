FROM python:3.9.10-alpine3.14
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install flask
COPY . /app
ENV FLASK_APP=app
CMD ["python","app.py"]

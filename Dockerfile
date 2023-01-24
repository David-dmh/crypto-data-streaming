FROM python:3.9.10-alpine3.14
WORKDIR /app
RUN pip install --upgrade pip
COPY . /app
RUN pip install -r requirements.txt
ENV FLASK_APP=app
CMD ["python", "app.py"]

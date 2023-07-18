FROM python:3.9.13

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=true
ENV FLASK_ENV=development

CMD ["sh", "-c", "sleep 5"]

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

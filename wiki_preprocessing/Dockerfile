FROM python:3.8-slim-buster
ENV db_password=mysql123
RUN apt-get update && apt-get dist-upgrade && \
    apt-get install -y default-mysql-client default-libmysqlclient-dev

COPY *.py *.ini *.sql requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt
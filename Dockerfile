FROM python:3.7

LABEL author="it@stuartmccoll.co.uk"

ADD . /app

WORKDIR /app

RUN apt-get update && apt-get install -f -y postgresql-client
RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=manage.py

RUN [ "chmod", "777", "wait-for-postgres.sh" ]

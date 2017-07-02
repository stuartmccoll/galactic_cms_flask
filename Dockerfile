FROM python:2.7

MAINTAINER Stuart McColl "contact@stuartmccoll.co.uk"

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]

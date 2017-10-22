FROM python:2.7

MAINTAINER Stuart McColl "it@stuartmccoll.co.uk"

ADD . /app

WORKDIR /app

RUN apt-get update && apt-get install -f -y postgresql-client
RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=manage.py

RUN [ "chmod", "777", "wait-for-postgres.sh" ]

# CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
# CMD [ "python", "manage.py", "runserver", "-h=0.0.0.0", "-p=5000"]

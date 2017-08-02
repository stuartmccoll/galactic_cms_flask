FROM python:2.7

MAINTAINER Stuart McColl "it@stuartmccoll.co.uk"

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=manage.py

RUN ["chmod", "+x", "wait-for-postgres.sh"]
# CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
CMD [ "python", "manage.py", "runserver", "-h=0.0.0.0", "-p=5000"]

ENTRYPOINT ["./wait-for-postgres.sh"]

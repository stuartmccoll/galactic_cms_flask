# galactic_cms_flask
A lightweight content management built using Python, Flask and Postgres.

# Installation
Build the Docker images using the following command within the root directory:

```
$ docker-compose build galactic-cms
```

After building the Docker images, simply run the Docker containers with the following command:

```
$ docker-compose up -d galactic-cms
```

# Database Migrations
Database migrations can be run using the below method.

Run the following command to enter the galactic-cms container:

```
$ docker exec -it galactic-cms bash
```

Within the container, the following command will run any database migrations that have not yet been run:

```
$ python manage.py db upgrade
```

The application can be accessed via the following URL: [http://0.0.0.0:5000/](http://0.0.0.0:5000/).
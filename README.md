# Galactic CMS [![Build Status](https://travis-ci.org/stuartmccoll/galactic_cms_flask.svg?branch=themes)](https://travis-ci.org/stuartmccoll/galactic_cms_flask)
A lightweight content management system built using Python, Flask and Postgres.

![Galactic Logo](http://stuartmccoll.co.uk/galactic.png)

# Installation
Build the Docker images using the following command within the root directory:

```bash
$ docker-compose build galactic-cms
```

After building the Docker images, simply run the Docker containers with the following command:

```bash
$ docker-compose up -d galactic-cms
```

---

# Database

## Database Migrations
Database migrations can be run using the below method.

Run the following command to enter the galactic-cms container:

```bash
$ docker exec -it galactic-cms bash
```

Within the container, the following command will run any database migrations that have not yet been run:

```bash
$ python manage.py db upgrade
```

## Database Access
To access the postgres database directly, you'll need to enter the database container before connecting to the database.

To do so, run the below commands:

```bash
$ docker exec -it -u postgres db-galactic-cms bash
```

You'll now be inside the database Docker container as the 'postgres' user.

```bash
$ psql <config.DBNAME>
```

Running the above command (where `<config.DBNAME>` is equal to the DBNAME environment variable inside the config.py file) will allow you direct access to the database.

The application can be accessed via the following URL: [http://0.0.0.0:5000/](http://0.0.0.0:5000/).
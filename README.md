# galactic_cms_flask
CMS using Python, Flask and Postgres.

# Installation
Build the Docker image using the following command:

```
$ docker build -t galactic-cms .
```

After building the Docker image, simply run the Docker container with the following command:

```
$ docker run -d -p 5000:5000 galactic-cms
```

The application can be accessed via the following URL: [http://0.0.0.0:5000/](http://0.0.0.0:5000/).
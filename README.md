# Kylin_API

This repository provides a 'production-ready' Flask API returning crypto price data from ~7 different sources.

The API has been set up for use with Python >= 3.7 and [Docker](https://www.docker.com/). 

## Running locally

To run the basic server, you'll need to install a few requirements. To do this, run:

```bash
pip install -r requirements/common.txt
```

This will install only the dependencies required to run the server. To boot up the 
default server, you can run:

```bash
bash bin/run.sh
```

This will start a [Gunicorn](https://gunicorn.org/) server that wraps the Flask app 
defined in `src/app.py`. Note that [this is one of the recommended ways of deploying a
Flask app 'in production'](https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/). 
The server shipped with Flask is [intended for development
purposes only](https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment).  

You should now be able to send:

```bash
curl localhost:8080/health
```

And receive the response `OK` and status code `200`. 

## Running with docker

Unsurprisingly, you'll need [Docker](https://www.docker.com/products/docker-desktop) 
installed to run this project with Docker. To build a containerised version of the API, 
run:

```bash
docker build . -t kylin-api
```

To launch the containerised app, run:

```bash
docker run -p 8080:8080 kylin-api
```

You should see your server boot up, and should be accessible as before.

## Testing the API

Testing the API is set up using `pytest`. To execute tests you can install the project's development dependencies with:

```bash
pip install -r requirements/develop.txt
```
Then from the root directory run:
```bash
pytest
```
This runs `test_api.py` which contains test functions. Add new funtions or files for extended testing functionality.

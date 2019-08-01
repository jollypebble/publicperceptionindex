# PPI Docker Environment

## Overview ##
This is a Docker Compose Environment for PPI Data Management. It includes the necessary backend architecture to run the persistant relational DB as well as the graphQL endpoints.
It also includes data scrapers and file parsers that can interact with these data stores.

## Commands ##

* Start Environment: `docker-compose up -d`
* Stop Environment: `docker-compose down -v`

## Query Data
You can check the Apollo Graphql server at `localhost:8000/graphql` or `127.0.0.1:8000/graphql`


### Using Docker

#### Prerequisities
 - Docker
You need to install docker on your pc. How to intall [docker](https://docs.docker.com/docker-for-mac/install/) ?

#### Run environment on local

```
$ git clone https://github.com/jollypebble/publicperceptionindex.git
$ cd docker-env/
(Rename .env.example to .env)
$ docker-compose up -d
```

You can stop the environment using
```
$ docker-compose down -v
```

You need to check db configuration in `.env` file.

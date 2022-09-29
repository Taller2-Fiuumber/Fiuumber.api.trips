# Fiuumber.api.trips

## Run app locally with docker

Run once:

``` bash
docker-compose up --build --force-recreate -d
```

Start server

``` bash
➜  Fiuumber.api.trip: docker ps
CONTAINER ID   IMAGE                 COMMAND                  CREATED          STATUS          PORTS                      NAMES
f875750a5542   fiuumberapitrip_web   "sh"                     18 seconds ago   Up 17 seconds   0.0.0.0:8080->8080/tcp     fiuumberapitrip_web_1
29ebfb1587a7   mongo:latest          "docker-entrypoint.s…"   19 seconds ago   Up 17 seconds   0.0.0.0:27017->27017/tcp   fiuumberapitrip_database_1➜  Fiuumber.api.trip git:(main) docker exec -it f875750a5542  sh


➜  Fiuumber.api.trip: docker exec -it f875750a5542  sh
/app # python -m uvicorn main:app --reload --host 0.0.0.0 --port 8080
INFO:     Will watch for changes in these directories: ['/app']
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
INFO:     Started reloader process [25] using StatReload
INFO:     Started server process [27]
INFO:     Waiting for application startup.
```

See swagger

``` bash
http://localhost:8080/docs
```

For more info: https://www.mongodb.com/languages/python/pymongo-tutorial

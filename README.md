# Fiuumber.api.trips

## Run app locally with docker

Start services:

``` bash
make start-services
```

Start FastAPI server

``` bash
➜  Fiuumber.api.trip: make exec
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

Stop services:

``` bash
make stop-services
```

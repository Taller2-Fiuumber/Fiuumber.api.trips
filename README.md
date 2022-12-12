# Fiuumber.api.trips

## Instalación y configuración

Start service locally for development:

Create containers:

``` bash
➜  docker-compose up --force-recreate -d

Recreating fiuumberapitrips_database_1 ... done
Recreating fiuumberapitrips_web_1      ... done
```

Enter containers:

``` bash
➜  docker exec -it fiuumberapiusers_web_1 bash
root@95d8af8d82d6:/app#
```

Start FastAPI server:

``` bash
root@abbc8e9b0781:/app# bash ./scripts/local-entrypoint.sh
```

See swagger

``` bash
http://localhost:8080/docs
```

Run tests:

``` bash
make test
```

Run format:

``` bash
make format
```

Run coverage:

``` bash
make coverage
```

# Nile API

API for the imaginary Nile marketplace for self published books.

This is a project created to try out FastAPI as the post promising ASGI server.

## Run locally

This project uses Docker Compose to manage the API & DB servers, the easiest way to get started is with:

```bash
docker-compose up
```

## Create a new migration

export PYTHONPATH='.'
alembic revision --autogenerate

## Apply the migration locally

alembic upgrade head

## Docs

Docs are created automatically & in dev mode are hosted at the path `/docs#/`.

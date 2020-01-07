# Nile API
API for the imaginary Nile marketplace for self published books.

This is a project created to try out FastAPI as the post promising ASGI server.

## Run locally
uvicorn api.main:app --reload

## Create a new migration
export PYTHONPATH='.'
alembic revision --autogenerate

## Apply the migration locally
alembic upgrade head

## Docs
Docs are created automatically & in dev mode are hosted at the path `/docs#/`.

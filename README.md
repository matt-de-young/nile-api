# Nile API
API for the imaginary Nile marketplace for self published books.

## Run locally
uvicorn api.main:app --reload

## Run in docker compose
docker-compose up

## Create a new migration
export PYTHONPATH='.'
alembic revision --autogenerate

## Apply the migration locally
alembic upgrade head

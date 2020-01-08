FROM python:3.7-alpine3.8

RUN apk update
RUN apk add --no-cache git gcc libc-dev make musl-dev postgresql-dev libffi-dev
RUN pip install pipenv 

COPY Pipfile* /app/
WORKDIR /app
RUN pipenv install --system --deploy --ignore-pipfile

CMD ["uvicorn", "api.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]

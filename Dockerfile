FROM python:3.7-alpine3.8

RUN apk update
RUN apk add --no-cache git gcc libc-dev make musl-dev postgresql-dev libffi-dev bash
RUN pip install pipenv 

WORKDIR /app

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY Pipfile* /
RUN pipenv install --system --deploy --ignore-pipfile

CMD ["uvicorn", "api.main:app", "--reload"]

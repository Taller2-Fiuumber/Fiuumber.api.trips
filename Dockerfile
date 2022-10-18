# syntax=docker/dockerfile:1

FROM python:3.10.7 as builder

ARG database_url
ARG database_name

ENV DB_NAME=${database_name}
ENV MONGODB_URL=${database_url}

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

RUN adduser -D myuser
USER myuser

CMD python -m uvicorn main:app --reload --host 0.0.0.0 --port ${PORT}

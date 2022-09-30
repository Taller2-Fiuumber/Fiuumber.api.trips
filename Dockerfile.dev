FROM python:3.10.7-alpine3.16

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

ENV PORT 8080

EXPOSE ${PORT}

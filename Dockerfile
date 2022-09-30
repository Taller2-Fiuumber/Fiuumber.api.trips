FROM python:3.10.7-alpine3.16
RUN mkdir /app
WORKDIR /app
COPY . /app

ARG database_url
ENV ME_CONFIG_MONGODB_URL=$database_url

RUN pip install -r requirements.txt

CMD python -m uvicorn main:app --reload --host 0.0.0.0 --port ${PORT}

# docuemntation: https://www.mongodb.com/languages/python/pymongo-tutorial

from fastapi import FastAPI
from pymongo import MongoClient
from os import environ
from src.services.routes import router as trip_router


MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Fiuumber API Trips"}


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(MONGODB_URL)
    app.database = app.mongodb_client[DB_NAME]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(trip_router, tags=["trips"], prefix="/api/trips")

from fastapi import APIRouter, Request, HTTPException
from pymongo import MongoClient
import src.services.fare_metrics as services
from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

router = APIRouter()


@router.get("/avg", response_description="Get trips fare average")
def find_fare_avg(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.find_fare_avg(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/min", response_description="Get trips fare minimum")
def find_fare_min(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.find_fare_min(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/max", response_description="Get trips fare minimum")
def find_fare_max(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.find_fare_max(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")

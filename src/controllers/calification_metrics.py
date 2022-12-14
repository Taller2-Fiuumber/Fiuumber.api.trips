from fastapi import APIRouter, Request, HTTPException
from pymongo import MongoClient
import src.services.calification_metrics as services
from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

router = APIRouter()


@router.get("/passenger/min", response_description="Get passenger min calification")
def get_calification_passenger_min(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.get_calification_passenger_min(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/passenger/max", response_description="Get passenger max calification")
def get_calification_passenger_max(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.get_calification_passenger_max(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/passenger/avg", response_description="Get passenger avg calification")
def get_calification_passenger_avg(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.get_calification_passenger_avg(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/driver/min", response_description="Get driver min calification")
def get_calification_driver_min(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.get_calification_driver_min(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/driver/max", response_description="Get driver max calification")
def get_calification_driver_max(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.get_calification_driver_max(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/driver/avg", response_description="Get driver avg calification")
def get_calification_driver_avg(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.get_calification_driver_avg(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")

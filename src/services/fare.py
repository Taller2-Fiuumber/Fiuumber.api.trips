from fastapi import APIRouter, Request, Response, HTTPException, status

from src.domain.fare_calculator import lineal

from pymongo import MongoClient

router = APIRouter()

from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

@router.get("/fare", response_description="Get a calculated fare from coordinates")
def get_trip_fare(from_latitude, to_latitude, from_longitude, to_longitude):
    try:
        fare = lineal(
            float(from_latitude),
            float(to_latitude),
            float(from_longitude),
            float(to_longitude),
        )
        return Response(content=str(fare), media_type="application/json")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))

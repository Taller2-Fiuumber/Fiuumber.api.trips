from fastapi import APIRouter, Request, HTTPException
from pymongo import MongoClient

from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

router = APIRouter()


@router.get("/passenger/min", response_description="Get passenger min calification")
def get_calification_passenger_min(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"reviewer": "PASSENGER"}}
    stage_trip_avg = {
        "$group": {
            "_id": "$_id",
            "driverId": {"$first": "$driverId"},
            "avg_stars": {"$avg": "$stars"},
        }
    }
    stage_trip_min = {"$group": {"_id": None, "min_stars": {"$min": "$avg_stars"}}}
    pipeline = [
        stage_match_terminated_status,
        stage_trip_avg,
        stage_trip_min,
    ]

    data = database["calification"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["min_stars"]
    raise HTTPException(status_code=500, detail=f"Internal error")


@router.get("/passenger/max", response_description="Get passenger max calification")
def get_calification_passenger_max(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"reviewer": "PASSENGER"}}
    stage_trip_avg = {
        "$group": {
            "_id": "$_id",
            "driverId": {"$first": "$driverId"},
            "avg_stars": {"$avg": "$stars"},
        }
    }
    stage_trip_max = {"$group": {"_id": None, "max_stars": {"$max": "$avg_stars"}}}
    pipeline = [
        stage_match_terminated_status,
        stage_trip_avg,
        stage_trip_max,
    ]

    data = database["calification"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["max_stars"]
    raise HTTPException(status_code=500, detail=f"Internal error")


@router.get("/passenger/avg", response_description="Get passenger avg calification")
def get_calification_passenger_avg(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"reviewer": "PASSENGER"}}
    stage_trip_avg = {
        "$group": {
            "_id": "$_id",
            "driverId": {"$first": "$driverId"},
            "avg_stars": {"$avg": "$stars"},
        }
    }
    stage_trip_avg_avg = {
        "$group": {"_id": None, "avg_stars_avg": {"$avg": "$avg_stars"}}
    }
    pipeline = [
        stage_match_terminated_status,
        stage_trip_avg,
        stage_trip_avg_avg,
    ]

    data = database["calification"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["avg_stars_avg"]
    raise HTTPException(status_code=500, detail=f"Internal error")


@router.get("/driver/min", response_description="Get driver min calification")
def get_calification_driver_min(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"reviewer": "DRIVER"}}
    stage_trip_avg = {
        "$group": {
            "_id": "$_id",
            "passengerId": {"$first": "$passengerId"},
            "avg_stars": {"$avg": "$stars"},
        }
    }
    stage_trip_min = {"$group": {"_id": None, "min_stars": {"$min": "$avg_stars"}}}
    pipeline = [
        stage_match_terminated_status,
        stage_trip_avg,
        stage_trip_min,
    ]

    data = database["calification"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["min_stars"]
    raise HTTPException(status_code=500, detail=f"Internal error")


@router.get("/driver/max", response_description="Get driver max calification")
def get_calification_driver_max(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"reviewer": "DRIVER"}}
    stage_trip_avg = {
        "$group": {
            "_id": "$_id",
            "passengerId": {"$first": "$passengerId"},
            "avg_stars": {"$avg": "$stars"},
        }
    }
    stage_trip_max = {"$group": {"_id": None, "max_stars": {"$max": "$avg_stars"}}}
    pipeline = [
        stage_match_terminated_status,
        stage_trip_avg,
        stage_trip_max,
    ]

    data = database["calification"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["max_stars"]
    raise HTTPException(status_code=500, detail=f"Internal error")


@router.get("/driver/avg", response_description="Get driver avg calification")
def get_calification_driver_avg(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"reviewer": "DRIVER"}}
    stage_trip_avg = {
        "$group": {
            "_id": "$_id",
            "passengerId": {"$first": "$passengerId"},
            "avg_stars": {"$avg": "$stars"},
        }
    }
    stage_trip_avg_avg = {
        "$group": {"_id": None, "avg_stars_avg": {"$avg": "$avg_stars"}}
    }
    pipeline = [
        stage_match_terminated_status,
        stage_trip_avg,
        stage_trip_avg_avg,
    ]

    data = database["calification"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["avg_stars_avg"]
    raise HTTPException(status_code=500, detail=f"Internal error")

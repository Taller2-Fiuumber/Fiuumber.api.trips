from fastapi import APIRouter, Request, HTTPException
from pymongo import MongoClient

from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

router = APIRouter()


@router.get(
    "/duration/min", response_description="Get trip duration minimum in minutes"
)
def get_trip_duration_min(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_trip_duration = {
        "$project": {"duration": {"$subtract": ["$finish", "$start"]}}
    }
    stage_trip_duration_min = {
        "$group": {"_id": None, "min_duration": {"$min": "$duration"}}
    }
    pipeline = [
        stage_match_terminated_status,
        stage_trip_duration,
        stage_trip_duration_min,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["min_duration"] / 60000
    raise HTTPException(status_code=500, detail=f"Internal error")


@router.get(
    "/duration/max", response_description="Get trip duration maximum in minutes"
)
def get_trip_duration_max(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_trip_duration = {
        "$project": {"duration": {"$subtract": ["$finish", "$start"]}}
    }
    stage_trip_duration_max = {
        "$group": {"_id": None, "max_duration": {"$max": "$duration"}}
    }
    pipeline = [
        stage_match_terminated_status,
        stage_trip_duration,
        stage_trip_duration_max,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["max_duration"] / 60000
    raise HTTPException(status_code=500, detail=f"Internal error")


@router.get(
    "/duration/avg", response_description="Get trip duration average in minutes"
)
def get_trip_duration_avg(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_trip_duration = {
        "$project": {"duration": {"$subtract": ["$finish", "$start"]}}
    }
    stage_trip_duration_avg = {
        "$group": {"_id": None, "avg_duration": {"$avg": "$duration"}}
    }
    pipeline = [
        stage_match_terminated_status,
        stage_trip_duration,
        stage_trip_duration_avg,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["avg_duration"] / 60000
    raise HTTPException(status_code=500, detail=f"Internal error")


@router.get("/status/count", response_description="Count trips by status")
def count_trips_by_status(status: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": status}}
    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [stage_match_terminated_status, stage_trip_count]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["count"]
    raise HTTPException(status_code=500, detail=f"Internal error")


@router.get("/count", response_description="Count trips")
def count_trips(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [stage_trip_count]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["count"]
    raise HTTPException(status_code=500, detail=f"Internal error")

from fastapi import APIRouter, Request, HTTPException
from pymongo import MongoClient

from os import environ

# MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = "Fiuumber"

def find_fare_avg(mongo_client):
    database = mongo_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_trip_duration_avg = {
        "$group": {"_id": None, "avg_final_price": {"$avg": "$finalPrice"}}
    }
    pipeline = [stage_match_terminated_status, stage_trip_duration_avg]

    data =database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["avg_final_price"]
    return None
        
def find_fare_min(mongo_client):

    database = mongo_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_trip_duration_min = {
        "$group": {"_id": None, "min_final_price": {"$min": "$finalPrice"}}
    }
    pipeline = [stage_match_terminated_status, stage_trip_duration_min]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["min_final_price"]
    return None


def find_fare_max(mongo_client):

    database = mongo_client[DB_NAME]
    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_trip_duration_max = {
        "$group": {"_id": None, "max_final_price": {"$max": "$finalPrice"}}
    }
    pipeline = [stage_match_terminated_status, stage_trip_duration_max]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["max_final_price"]
    return None

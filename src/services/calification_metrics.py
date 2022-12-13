from fastapi import APIRouter, Request, HTTPException
from pymongo import MongoClient

from os import environ

# DB_NAME = environ["DB_NAME"]
DB_NAME = "Fiuumber"

def get_calification_passenger_min(mongo_client):
    database = mongo_client[DB_NAME]

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
    return None


def get_calification_passenger_max(mongo_client):
    database = mongo_client[DB_NAME]

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
    return None


def get_calification_passenger_avg(mongo_client):
    database = mongo_client[DB_NAME]

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
    return None


def get_calification_driver_min(mongo_client):
    database = mongo_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"reviewer": "PASSENGER"}}
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
    return None


def get_calification_driver_max(mongo_client):
    database = mongo_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"reviewer": "PASSENGER"}}
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
    return None


def get_calification_driver_avg(mongo_client):
    database = mongo_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"reviewer": "PASSENGER"}}
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
    return None

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from src.domain.trip import Trip, TripUpdate
import src.domain.status as trip_status
import datetime

from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

router = APIRouter()


@router.get(
    "/trip/{id}/status", response_description="Get a single trip's status by id"
)
def find_trip_status(id: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    if (trip := database["trips"].find_one({"_id": id})) is not None:
        return trip["status"]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )

@router.put("/trip/{id}/status", response_description="Update a trip status")
def update_trip_status(id: str, request: Request, body=Body(...)):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]

        database["trips"].update_one(
            {"_id": id},
            {"$set": {"status": body.get("status")}},
        )

        stored_trip = database["trips"].find_one({"_id": id})

        return stored_trip

    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Error updating status {id} trip: {str(ex)}"
        )

@router.put("/trip/{id}/status/next", response_description="Update a trip status")
def update_trip_status(id: str, request: Request, body=Body(...)):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]

        trip = database["trips"].find_one({"_id": id})

        if trip is not None:
            status = trip_status.StatusFactory(trip["status"])

            if status.name() == trip_status.DriverAssigned().name():
                database["trips"].update_one(
                    {"_id": id},
                    {"$set":
                        {
                        "status": status.next().name(),
                        "start": datetime.datetime.now(),
                        }
                    },
                )
            elif status == trip_status.InProgress():
                database["trips"].update_one(
                    {"_id": id},
                    {"$set":
                        {
                        "status": status.next().name(),
                        "finish": datetime.datetime.now(),
                        }
                    },
                )
            else:
                database["trips"].update_one(
                    {"_id": id},
                    {"$set":{"status": status.next().name()}},
                )

        stored_trip = database["trips"].find_one({"_id": id})

        return stored_trip

    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Error updating status {id} trip: {str(ex)}"
        )

@router.put("/trip/{id}/status/cancel", response_description="Update a trip status")
def update_trip_status(id: str, request: Request, body=Body(...)):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]

        trip = database["trips"].find_one({"_id": id})
        if trip is not None:
            status = StatusFactory(trip["status"])
            database["trips"].update_one(
                {"_id": id},
                {"$set": {"status": status.cancel()}},
            )
            # TO-DO

        stored_trip = database["trips"].find_one({"_id": id})

        return stored_trip

    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Error updating status {id} trip: {str(ex)}"
        )

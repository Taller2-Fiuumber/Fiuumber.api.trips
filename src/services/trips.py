from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from src.domain.trip import Trip, TripUpdate
import src.domain.status as trip_status

from os import environ

# DB_NAME = environ["DB_NAME"]
DB_NAME = "Fiuumber"



def create_trip(mongo_client, trip):
    database = mongo_client[DB_NAME]

    new_trip = database["trips"].insert_one(trip)
    created_trip = database["trips"].find_one({"_id": new_trip.inserted_id})

    if created_trip is not None:
        return created_trip
    return None



def list_trips(mongo_client):
    database = mongo_client[DB_NAME]

    _trips = database["trips"].find()
    trips = list(_trips)
    return trips


def find_trip_by_id(id: str, mongo_client):
    database = mongo_client[DB_NAME]

    if (trip := database["trips"].find_one({"_id": id})) is not None:
        return trip
    return None



def duration_by_id(id: str, mongo_client):
    database = mongo_client[DB_NAME]
    trip = database["trips"].find_one({"_id": id})
    if trip is not None:
        status = trip_status.StatusFactory(trip["status"])
        if status != trip_status.Terminated():
            return -1
        else:
            return (trip["finish"] - trip["start"]).seconds / 60
    return None



async def patch_item(id: str, body, mongo_client):
    database = mongo_client[DB_NAME]
    stored_trip = database["trips"].find_one({"_id": id})
    if stored_trip is not None:
        update_data = body
        updated_item = stored_trip.copy(update=update_data)
        update_result = database["trips"].update_one(
            {"_id": id}, {"$set": jsonable_encoder(updated_item)}
        )
        return update_result
    return None


def update_trip(id: str,mongo_client, trip):
    database = mongo_client[DB_NAME]

    trip = {k: v for k, v in trip.items() if v is not None}
    if len(trip) >= 1:
        update_result = database["trips"].update_one({"_id": id}, {"$set": trip})

        if not update_result or update_result.modified_count == 0:
            return None

    if (existing_trip := database["trips"].find_one({"_id": id})) is not None:
        return existing_trip

    return None



def delete_trip(id: str, mongo_client):
    database = mongo_client[DB_NAME]

    delete_result = database["trips"].delete_one({"_id": id})
    return delete_result.deleted_count



def delete_all_trip( mongo_client):
    database = mongo_client[DB_NAME]

    delete_result = database["trips"].delete_many({})
    if not delete_result:
        return None

    return delete_result.deleted_count



def find_trip_status(id: str, mongo_client):
    database = mongo_client[DB_NAME]

    if (trip := database["trips"].find_one({"_id": id})) is not None:
        return trip["status"]
    return None


async def patch_item(id: str, body, mongo_client):
    database = mongo_client[DB_NAME]
    if (stored_trip) is not None:
        return update_result
    return None



def assign_driver(id: str,driver_id,mongo_client):
   
        database = mongo_client[DB_NAME]

        stored_trip = database["trips"].find_one({"_id": id})
        if stored_trip["status"] != "REQUESTED":
            raise Exception("Cannot assign driver to a non pending trip")

        database["trips"].update_one(
            {"_id": id},
            {"$set": {"driverId": driver_id, "status": "DRIVER_ASSIGNED"}},
        )

        stored_trip = database["trips"].find_one({"_id": id})

        if stored_trip is not None:
            return stored_trip
        return None
    



def trips_by_passenger_id(userId: str, skip: int, limit: int,mongo_client):
    database = mongo_client[DB_NAME]
    trips = database["trips"].find({"passengerId": userId}).skip(skip).limit(limit)
    if trips is not None:
        return list(trips)
    return None


def trips_by_driver_id(userId: str, skip: int, limit: int, mongo_client):
    database = mongo_client[DB_NAME]
    trips = database["trips"].find({"driverId": userId}).skip(skip).limit(limit)
    if trips is not None:
        return list(trips)
    return None

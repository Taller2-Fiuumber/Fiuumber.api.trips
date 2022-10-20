from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from pymongo import MongoClient

from src.domain.trip import Trip, TripUpdate
from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

router = APIRouter()


@router.post(
    "/trip",
    response_description="Create a new trip",
    status_code=status.HTTP_201_CREATED,
    response_model=Trip,
)
def create_trip(request: Request, trip: Trip = Body(...)):
    mongo_client= MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    trip = jsonable_encoder(trip)
    new_trip = database["trips"].insert_one(trip)
    created_trip = database["trips"].find_one({"_id": new_trip.inserted_id})

    if created_trip is not None:
        return created_trip
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )

@router.get("/trips", response_description="List all trips", response_model=List[Trip])
def list_trips(request: Request):
    mongo_client= MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    _trips = database["trips"].find(limit=10)
    trips = list(_trips)
    return trips


@router.get(
    "/trip/id={id}", response_description="Get a single trip by id", response_model=Trip
)
def find_trip(id: str, request: Request):
    mongo_client= MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    if (trip := database["trips"].find_one({"_id": id})) is not None:
        return trip
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.put("/trip/id={id}", response_description="Update a trip", response_model=Trip)
def update_trip(id: str, request: Request, trip: TripUpdate = Body(...)):
    mongo_client= MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    trip = {k: v for k, v in trip.dict().items() if v is not None}
    if len(trip) >= 1:
        update_result = database["trips"].update_one(
            {"_id": id}, {"$set": trip}
        )

        if not update_result or update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trip with ID {id} not found",
            )

    if (
        existing_trip := database["trips"].find_one({"_id": id})
    ) is not None:
        return existing_trip

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.delete("/trip/id={id}", response_description="Delete a trip")
def delete_trip(id: str, request: Request, response: Response):
    mongo_client= MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    delete_result = database["trips"].delete_one({"_id": id})

    if not delete_result or delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )

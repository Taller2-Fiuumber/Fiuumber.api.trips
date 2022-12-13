from fastapi import APIRouter, Body, Request, HTTPException, status
from pymongo import MongoClient

import src.domain.status as trip_status
import datetime
import src.services.trips_status as services

from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

router = APIRouter()


@router.get(
    "/trip/{id}/status", response_description="Get a single trip's status by id"
)
def find_trip_status(id: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    trip = find_trip_status(id, mongo_client)
    if trip is not None:
        return trip
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.put("/trip/{id}/status", response_description="Update a trip status")
def update_trip_status(id: str, request: Request, body=Body(...)):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        status = body.get("status")

        
        stored_trip = services.update_trip_status(id, mongo_client,status)

        return stored_trip

    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Error updating status {id} trip: {str(ex)}"
        )


@router.put("/trip/{id}/status/next", response_description="Update a trip status")
def update_trip_to_next_status(id: str, request: Request):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)

        trip = services.update_trip_to_next_status(id, mongo_client)

        if trip is not None:

            return trip

    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Error updating status {id} trip: {str(ex)}"
        )

#//////////////////la quede aca
@router.put("/trip/{id}/status/cancel", response_description="Update a trip status")
def cancel_trip(id: str, request: Request, body=Body(...)):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)

        trip = services.cancel_trip(id, mongo_client)
        if trip is not None:

            return trip

    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Error updating status {id} trip: {str(ex)}"
        )

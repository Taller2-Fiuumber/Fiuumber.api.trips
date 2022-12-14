from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from src.domain.trip import Trip, TripUpdate
import src.services.trips as services

from os import environ

MONGODB_URL = environ["MONGODB_URL"]

router = APIRouter()


@router.post(
    "/trip",
    response_description="Create a new trip",
    status_code=status.HTTP_201_CREATED,
)
def create_trip(request: Request, trip: Trip = Body(...)):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    trip = jsonable_encoder(trip)
    created_trip = services.create_trip(mongo_client, trip)

    if created_trip is not None:
        return created_trip
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.get("/trips", response_description="List all trips")
def list_trips(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    trips = services.list_trips(mongo_client)
    return trips


@router.get("/trip/{id}", response_description="Get a single trip by id")
def find_trip_by_id(id: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    trip = services.find_trip_by_id(id, mongo_client)
    if trip is not None:
        return trip
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.get(
    "/trip/{id}/duration", response_description="Get duration in minutes of trip by id"
)
def duration_by_id(id: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    duration = services.duration_by_id(id, mongo_client)
    if duration == -1:
        raise HTTPException(
            status_code=400, detail=f"Trip {id} status is not terminated"
        )
    elif duration is not None:
        return duration
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.put("/trip/{id}", response_description="Update a trip")
def update_trip(id: str, request: Request, trip: TripUpdate = Body(...)):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    trip = {k: v for k, v in trip.dict().items() if v is not None}

    updated_trip = services.update_trip(id, mongo_client, trip)
    if updated_trip is not None:
        return updated_trip
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.delete("/trip/{id}", response_description="Delete a trip")
def delete_trip(id: str, request: Request, response: Response):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    delete_result = services.delete_trip(id, mongo_client)

    if not delete_result:
        return delete_result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.delete("/trips", response_description="Delete all trips")
def delete_all_trip(request: Request, response: Response):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    delete_result = services.delete_all_trip(mongo_client)
    if not delete_result:
        return None

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trips not found")


@router.get(
    "/trip/{id}/status", response_description="Get a single trip's status by id"
)
def find_trip_status(id: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    trip = services.find_trip_status(id, mongo_client)
    if trip is not None:
        return trip
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.patch("/trip/{id}")
async def patch_item(id: str, body=Body(...)):
    _body = body.dict(exclude_unset=True)
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    stored_trip = services.patch_item(id, _body, mongo_client)

    if stored_trip is not None:
        return stored_trip
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.post(
    "/trip/{id}/assign-driver",
    response_description="Assign driver to a trip",
)
def assign_driver(id: str, request: Request, body=Body(...)):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)

        driver_id = body.get("driverId")
        stored_trip = services.assign_driver(id, driver_id, mongo_client)

        if stored_trip is not None:
            return stored_trip

    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Error updating status {id} trip: {str(ex)}"
        )


@router.get("/passenger/{userId}", response_description="Get trips by passenger id")
def trips_by_passenger_id(userId: str, skip: int, limit: int, in_progress: bool, request: Request):

    trips = services.trips_by_passenger_id(userId, skip, limit, in_progress)
    if trips is not None:
        return trips
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Trips with passenger id {userId} not found",
    )


@router.get("/driver/{userId}", response_description="Get trips by driver id")
def trips_by_driver_id(userId: str, skip: int, limit: int, in_progress: bool, request: Request):
    
    trips = services.trips_by_driver_id(userId, skip, limit, in_progress)
    if trips is not None:
        return trips
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Trips with driver id {userId} not found",
    )

@router.get(
    "/passenger/{userId}/count", response_description="Count trips by passenger id"
)
def total_trips_by_passenger_id(userId: str):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    trips = services.total_trips_by_passenger_id(userId, mongo_client)
    if trips != -1:
        return trips
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Trips with passenger id {userId} not found",
   )

@router.get(
    "/driver/{userId}/count", response_description="Count trips by driver id"
)
def total_trips_by_driver_id(userId: str):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    trips = services.total_trips_by_driver_id(userId, mongo_client)
    if trips != -1:
        return trips
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Trips with driver id {userId} not found",
   )
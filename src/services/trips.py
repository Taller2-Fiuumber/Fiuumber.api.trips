from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from src.domain.trip import Trip, TripUpdate
import src.domain.status as trip_status

from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

router = APIRouter()


@router.post(
    "/trip",
    response_description="Create a new trip",
    status_code=status.HTTP_201_CREATED,
)
def create_trip(request: Request, trip: Trip = Body(...)):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    trip = jsonable_encoder(trip)
    new_trip = database["trips"].insert_one(trip)
    created_trip = database["trips"].find_one({"_id": new_trip.inserted_id})

    if created_trip is not None:
        return created_trip
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.get("/trips", response_description="List all trips")
def list_trips(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    _trips = database["trips"].find()
    trips = list(_trips)
    return trips


@router.get("/trip/{id}", response_description="Get a single trip by id")
def find_trip_by_id(id: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    if (trip := database["trips"].find_one({"_id": id})) is not None:
        return trip
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.get(
    "/trip/{id}/duration", response_description="Get duration in minutes of trip by id"
)
def duration_by_id(id: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]
    trip = database["trips"].find_one({"_id": id})
    if trip is not None:
        status = trip_status.StatusFactory(trip["status"])
        if status != trip_status.Terminated():
            raise HTTPException(
                status_code=400, detail=f"Trip {id} status is not terminated"
            )
        else:
            return (trip["finish"] - trip["start"]).seconds / 60
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.put("/trip/{id}", response_description="Update a trip")
def update_trip(id: str, request: Request, trip: TripUpdate = Body(...)):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    trip = {k: v for k, v in trip.dict().items() if v is not None}
    if len(trip) >= 1:
        update_result = database["trips"].update_one({"_id": id}, {"$set": trip})

        if not update_result or update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trip with ID {id} not found",
            )

    if (existing_trip := database["trips"].find_one({"_id": id})) is not None:
        return existing_trip

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.delete("/trip/{id}", response_description="Delete a trip")
def delete_trip(id: str, request: Request, response: Response):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    delete_result = database["trips"].delete_one({"_id": id})

    if not delete_result or delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.delete("/trips", response_description="Delete all trips")
def delete_all_trip(id: str, request: Request, response: Response):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    delete_result = database["trips"].delete()
    if not delete_result:
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


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


@router.patch("/trip/{id}")
async def patch_item(id: str, body=Body(...)):
    print(id)
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]
    stored_trip = database["trips"].find_one({"_id": id})
    if (stored_trip) is not None:
        update_data = body.dict(exclude_unset=True)
        updated_item = stored_trip.copy(update=update_data)
        update_result = database["trips"].update_one(
            {"_id": id}, {"$set": jsonable_encoder(updated_item)}
        )
        return update_result
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
        database = mongo_client.mongodb_client[DB_NAME]

        stored_trip = database["trips"].find_one({"_id": id})

        if stored_trip["status"] != "REQUESTED":
            raise Exception("Cannot assign driver to a non pending trip")

        database["trips"].update_one(
            {"_id": id},
            {"$set": {"driverId": body.get("driverId"), "status": "DRIVER_ASSIGNED"}},
        )

        stored_trip = database["trips"].find_one({"_id": id})

        return stored_trip
    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Error updating status {id} trip: {str(ex)}"
        )


@router.get(
    "/passenger/{userId}", response_description="Get trips by passenger id"
)
def trips_by_passenger_id(userId: str, skip: int, limit: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]
    trips = database["trips"].find({"passengerId": userId}).skip(skip).limit(limit)
    if trips is not None:
        return list(trips)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Trips with passenger id {userId} not found",
    )


@router.get("/driver/{userId}", response_description="Get trips by driver id")
def trips_by_driver_id(userId: str, skip: int, limit: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]
    trips = database["trips"].find({"driverId": userId}).skip(skip).limit(limit)
    if trips is not None:
        return list(trips)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Trips with driver id {userId} not found",
    )

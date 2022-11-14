from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from src.domain.trip import Trip, TripUpdate
from src.domain.fare_calculator import lineal
from src.domain.calification import Calification

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

    _trips = database["trips"].find(limit=10)
    trips = list(_trips)
    return trips


@router.get("/trip/{id}", response_description="Get a single trip by id")
def find_trip(id: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    if (trip := database["trips"].find_one({"_id": id})) is not None:
        return trip
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


@router.get("/fare", response_description="Get a calculated fare from coordinates")
def get_trip_fare(from_latitude, to_latitude, from_longitude, to_longitude):
    try:
        fare = lineal(
            float(from_latitude),
            float(to_latitude),
            float(from_longitude),
            float(to_longitude),
        )
        return Response(content=str(fare), media_type="application/json")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))


@router.post(
    "/calification",
    response_description="Create a users's comment to a trip",
    status_code=status.HTTP_201_CREATED,
)
def create_calification_passenger(
    request: Request, calification: Calification = Body(...)
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    calification = jsonable_encoder(calification)
    new_calification = database["calification"].insert_one(calification)
    created_calification = database["calification"].find_one(
        {"_id": new_calification.inserted_id}
    )

    if created_calification is not None:
        return created_calification


@router.get("/calification", response_description="Get a single trip by id")
def find_califications(skip: int, limit: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    _califications = database["calification"].find().skip(skip).limit(limit)
    return list(_califications)


@router.get("/calification/passenger", response_description="Get a single trip by id")
def find_califications_of_passenger(skip: int, limit: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    _califications = (
        database["calification"].find({"reviewer": "PASSENGER"}).skip(skip).limit(limit)
    )
    return list(_califications)


@router.get("/calification/driver", response_description="Get a single trip by id")
def find_califications_of_driver(skip: int, limit: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    _califications = (
        database["calification"].find({"reviewer": "DRIVER"}).skip(skip).limit(limit)
    )
    return list(_califications)


@router.get(
    "/calification/passenger/tripId/{tripId}",
    response_description="Get a single trip by id",
)
def find_califications_of_passenegr_by_tripId(
    tripId: str, skip: int, limit: int, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    _califications = (
        database["calification"]
        .find({"tripId": tripId, "reviewer": "PASSENGER"})
        .skip(skip)
        .limit(limit)
    )
    return list(_califications)


@router.get(
    "/calification/driver/tripId/{tripId}",
    response_description="Get a single trip by id",
)
def find_califications_of_driver_by_tripId(
    tripId: str, skip: int, limit: int, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    _califications = (
        database["calification"]
        .find({"tripId": tripId, "reviewer": "DRIVER"})
        .skip(skip)
        .limit(limit)
    )
    return list(_califications)


@router.get(
    "/calification/passenger/{passengerId}/tripId/{tripId}",
    response_description="Get a single trip by id",
)
def find_califications_of_passenegr_by_tripId_and_by_driver(
    passengerId: str, tripId: str, skip: int, limit: int, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    _califications = (
        database["calification"]
        .find({"tripId": tripId, "reviewer": "PASSENGER", "passengerId": passengerId})
        .skip(skip)
        .limit(limit)
    )
    return list(_califications)


@router.get(
    "/calification/driver/{driverId}/tripId/{tripId}",
    response_description="Get a single trip by id",
)
def find_califications_of_driver_by_tripId_and_by_driverId(
    driverId: str, tripId: str, skip: int, limit: int, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    _califications = (
        database["calification"]
        .find({"tripId": tripId, "reviewer": "DRIVER", "driverId": driverId})
        .skip(skip)
        .limit(limit)
    )
    return list(_califications)


@router.get(
    "/calification/passenger/{passengerId}",
    response_description="Get a single trip by id",
)
def find_califications_of_passenegr_by_passengerId(
    passengerId: str, skip: int, limit: int, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    _califications = (
        database["calification"]
        .find({"reviewer": "PASSENGER", "passengerId": passengerId})
        .skip(skip)
        .limit(limit)
    )
    return list(_califications)


@router.get(
    "/calification/driver/{driverId}/avg", response_description="Get a single trip by id"
)
def find_califications_mean_of_driver_by_driverId(
    driverId: str, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    pipeline = [
                {'$match' : { 'driverId' : driverId } },
                {'$group': {
                    '_id': "$driverId",
                    'avg_stars': {'$avg': '$stars'},
                }},
                ]

    return list(database["calification"].aggregate(pipeline))

@router.get(
    "/calification/passenger/{passengerId}/avg", response_description="Get a single trip by id"
)
def find_califications_mean_of_driver_by_passengerId(
    passengerId: str, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    pipeline = [
                {'$match' : { 'passengerId' : passengerId } },
                {'$group': {
                    '_id': "$passengerId",
                    'avg_stars': {'$avg': '$stars'},
                }},
                ]

    return list(database["calification"].aggregate(pipeline))


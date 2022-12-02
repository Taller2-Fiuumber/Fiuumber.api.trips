from fastapi import APIRouter, Body, Request, status
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from src.domain.calification import Calification

from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

router = APIRouter()


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
    response_description="Get califications",
)
def find_califications_of_passenger_by_tripId(
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
    response_description="Get califications",
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
    response_description="Get califications",
)
def find_califications_of_passenger_by_tripId_and_by_driver(
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
    response_description="Get califications",
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
    response_description="Find califications of passenger by passengerId",
)
def find_califications_of_passenger_by_passengerId(
    passengerId: str, skip: int, limit: int, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    _califications = (
        database["calification"]
        .find({"reviewer": "DRIVER", "passengerId": passengerId})
        .skip(skip)
        .limit(limit)
    )
    return list(_califications)


@router.get(
    "/calification/driver/{driverId}",
    response_description="Find califications of driver by driverId",
)
def find_califications_of_driver_by_driverId(
    driverId: str, skip: int, limit: int, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    _califications = (
        database["calification"]
        .find({"reviewer": "PASSENGER", "driverId": driverId})
        .skip(skip)
        .limit(limit)
    )
    return list(_califications)


@router.get(
    "/calification/driver/{driverId}/avg",
    response_description="Get califications",
)
def find_califications_mean_of_driver_by_driverId(driverId: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    pipeline = [
        {"$match": {"driverId": driverId}},
        {
            "$group": {
                "_id": "$driverId",
                "avg_stars": {"$avg": "$stars"},
            }
        },
    ]

    return list(database["calification"].aggregate(pipeline))


@router.get(
    "/calification/passenger/{passengerId}/avg",
    response_description="Get califications",
)
def find_califications_mean_of_driver_by_passengerId(
    passengerId: str, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    pipeline = [
        {"$match": {"passengerId": passengerId}},
        {
            "$group": {
                "_id": "$passengerId",
                "avg_stars": {"$avg": "$stars"},
            }
        },
    ]

    return list(database["calification"].aggregate(pipeline))

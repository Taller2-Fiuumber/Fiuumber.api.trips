from pymongo import MongoClient
from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

mongo_client = MongoClient(MONGODB_URL, connect=False)
database = mongo_client.mongodb_client[DB_NAME]


def get_trip_by_id(trip_id):
    trip = database["trips"].find_one({"_id": trip_id})
    return trip

def get_trips_driver(driver_id, skip=0, limit=1000, only_in_progress = False):

    # No debería haber más de uno en progreso
    if (only_in_progress):
        skip = 0
        limit = 1

    filters = (
        {
            "$and": [
                {"driverId": driver_id},
                {
                    "status": {
                        "$in": [
                            "REQUESTED",
                            "DRIVER_ASSIGNED",
                            "DRIVER_ARRIVED",
                            "IN_PROGRESS",
                        ]
                    }
                },
            ]
        }
        if only_in_progress
        else {"driverId": driver_id}
    )

    trips = database["trips"].find(filters).skip(skip).limit(limit).sort("start", -1)

    return list(trips)

def get_trips_passenger(passenger_id, skip=0, limit=1000, only_in_progress = False):

    # No debería haber más de uno en progreso
    if (only_in_progress):
        skip = 0
        limit = 1

    filters = (
        {
            "$and": [
                {"passengerId": passenger_id},
                {
                    "status": {
                        "$in": [
                            "REQUESTED",
                            "DRIVER_ASSIGNED",
                            "DRIVER_ARRIVED",
                            "IN_PROGRESS",
                        ]
                    }
                },
            ]
        }
        if only_in_progress
        else {"passengerId": passenger_id}
    )

    trips = database["trips"].find(filters).skip(skip).limit(limit).sort("start", -1)

    return list(trips)
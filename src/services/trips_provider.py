from os import environ

DB_NAME = environ["DB_NAME"] if "DB_NAME" in environ else "Fiuumber"


def get_trip_by_id(mongo_client, trip_id):
    database = mongo_client[DB_NAME]

    trip = database["trips"].find_one({"_id": trip_id})

    return trip


def get_trips_driver(
    mongo_client, driver_id, skip=0, limit=1000, only_in_progress=False
):
    database = mongo_client[DB_NAME]
    # No debería haber más de uno en progreso
    if only_in_progress:
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


def get_trips_passenger(
    mongo_client, passenger_id, skip=0, limit=1000, only_in_progress=False
):
    database = mongo_client[DB_NAME]

    # No debería haber más de uno en progreso
    if only_in_progress:
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

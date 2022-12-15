from os import environ

DB_NAME = environ["DB_NAME"] if "DB_NAME" in environ else "Fiuumber"


def create_calification_passenger(mongo_client, calification):
    database = mongo_client[DB_NAME]

    new_calification = database["calification"].insert_one(calification)
    created_calification = database["calification"].find_one(
        {"_id": new_calification.inserted_id}
    )

    if created_calification is not None:
        return created_calification
    return None


def find_califications(skip: int, limit: int, mongo_client):
    database = mongo_client[DB_NAME]

    _califications = database["calification"].find().skip(skip).limit(limit)
    return list(_califications)


def find_califications_of_passenger(skip: int, limit: int, mongo_client):
    database = mongo_client[DB_NAME]

    _califications = (
        database["calification"].find({"reviewer": "PASSENGER"}).skip(skip).limit(limit)
    )
    return list(_califications)


def find_califications_of_driver(skip: int, limit: int, mongo_client):
    database = mongo_client[DB_NAME]

    _califications = (
        database["calification"].find({"reviewer": "DRIVER"}).skip(skip).limit(limit)
    )
    return list(_califications)


def find_califications_of_passenger_by_tripId(
    tripId: str, skip: int, limit: int, mongo_client
):
    database = mongo_client[DB_NAME]

    _califications = (
        database["calification"]
        .find({"tripId": tripId, "reviewer": "PASSENGER"})
        .skip(skip)
        .limit(limit)
    )
    return list(_califications)


def find_califications_of_driver_by_tripId(
    tripId: str, skip: int, limit: int, mongo_client
):
    database = mongo_client[DB_NAME]

    _califications = (
        database["calification"]
        .find({"tripId": tripId, "reviewer": "DRIVER"})
        .skip(skip)
        .limit(limit)
    )
    return list(_califications)


def find_califications_of_passenger_by_tripId_and_by_passengerId(
    passengerId: str, tripId: str, skip: int, limit: int, mongo_client
):
    database = mongo_client[DB_NAME]

    _califications = (
        database["calification"]
        .find({"tripId": tripId, "reviewer": "PASSENGER", "passengerId": passengerId})
        .skip(skip)
        .limit(limit)
    )
    return list(_califications)


def find_califications_of_driver_by_tripId_and_by_driverId(
    driverId: str, tripId: str, skip: int, limit: int, mongo_client
):
    database = mongo_client[DB_NAME]

    _califications = (
        database["calification"]
        .find({"tripId": tripId, "reviewer": "DRIVER", "driverId": driverId})
        .skip(skip)
        .limit(limit)
    )
    return list(_califications)


def find_califications_of_passenger_by_passengerId(
    passengerId: str, skip: int, limit: int, mongo_client
):
    database = mongo_client[DB_NAME]

    _califications = (
        database["calification"]
        .find({"reviewer": "DRIVER", "passengerId": passengerId})
        .skip(skip)
        .limit(limit)
    )
    return list(_califications)


def find_califications_of_driver_by_driverId(
    driverId: str, skip: int, limit: int, mongo_client
):
    database = mongo_client[DB_NAME]

    _califications = (
        database["calification"]
        .find({"reviewer": "PASSENGER", "driverId": driverId})
        .skip(skip)
        .limit(limit)
    )
    return list(_califications)


def find_califications_mean_of_driver_by_driverId(driverId: str, mongo_client):
    database = mongo_client[DB_NAME]

    pipeline = [
        {"$match": {"driverId": driverId, "reviewer": "PASSENGER"}},
        {
            "$group": {
                "_id": "$driverId",
                "avg_stars": {"$avg": "$stars"},
            }
        },
    ]
    data = database["calification"].aggregate(pipeline)

    if data is None:
        return None
    return list(data)[0]["avg_stars"]


def find_califications_mean_of_driver_by_passengerId(passengerId: str, mongo_client):
    database = mongo_client[DB_NAME]

    pipeline = [
        {"$match": {"passengerId": passengerId, "reviewer": "DRIVER"}},
        {
            "$group": {
                "_id": "$passengerId",
                "avg_stars": {"$avg": "$stars"},
            }
        },
    ]
    data = database["calification"].aggregate(pipeline)
    if data is None:
        return None
    return list(data)[0]["avg_stars"]

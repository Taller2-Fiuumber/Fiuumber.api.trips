import src.domain.status as trip_status
from fastapi.encoders import jsonable_encoder
from os import environ
import src.services.trips_provider as trips_provider
from src.utils.notifications_processor import (
    notify_for_assigned_driver,
    notify_for_new_trip,
)

DB_NAME = environ["DB_NAME"] if "DB_NAME" in environ else "Fiuumber"


def create_trip(mongo_client, trip):
    database = mongo_client[DB_NAME]

    new_trip = database["trips"].insert_one(trip)
    created_trip = database["trips"].find_one({"_id": new_trip.inserted_id})

    try:
        notify_for_new_trip(new_trip.inserted_id)
    except Exception as ex:
        print(
            f"[ERROR -> Continue] send notification for trip requested {id} reason: {str(ex)}"
        )
        pass

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


def update_trip(id: str, mongo_client, trip):
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


def delete_all_trip(mongo_client):
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


def assign_driver(id: str, driver_id, mongo_client):

    database = mongo_client[DB_NAME]

    stored_trip = database["trips"].find_one({"_id": id})
    if stored_trip["status"] != "REQUESTED":
        raise Exception("Cannot assign driver to a non pending trip")

    database["trips"].update_one(
        {"_id": id},
        {"$set": {"driverId": driver_id, "status": "DRIVER_ASSIGNED"}},
    )

    try:
        notify_for_assigned_driver(mongo_client, id)
    except Exception as ex:
        print(
            f"[ERROR -> Continue] send notification for driver assigned {id} reason: {str(ex)}"
        )
        pass

    stored_trip = database["trips"].find_one({"_id": id})

    if stored_trip is not None:
        return stored_trip
    return None


def trips_by_passenger_id(
    mongo_client, userId: str, skip: int, limit: int, in_progress: bool = False
):
    try:
        return trips_provider.get_trips_passenger(
            mongo_client, userId, skip=skip, limit=limit, only_in_progress=in_progress
        )
    except Exception:
        return None


def total_trips_by_passenger_id(userId: str, mongo_client):
    database = mongo_client[DB_NAME]

    trips = database["trips"].find({"passengerId": userId})
    if trips is not None:
        return len(list(trips))
    return -1


def trips_by_driver_id(
    mongo_client, userId: str, skip: int, limit: int, in_progress: bool = False
):
    try:
        return trips_provider.get_trips_driver(
            mongo_client, userId, skip=skip, limit=limit, only_in_progress=in_progress
        )
    except Exception:
        return None


def total_trips_by_driver_id(userId: str, mongo_client):
    database = mongo_client[DB_NAME]

    trips = database["trips"].find({"driverId": userId})
    if trips is not None:
        return len(list(trips))
    return -1

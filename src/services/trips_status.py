import src.domain.status as trip_status
import datetime


# DB_NAME = environ["DB_NAME"]
DB_NAME = "Fiuumber"


def find_trip_status(id: str, mongo_client):
    database = mongo_client[DB_NAME]

    if (trip := database["trips"].find_one({"_id": id})) is not None:
        return trip["status"]
    return None


def update_trip_status(id: str, mongo_client, status):

    database = mongo_client[DB_NAME]

    database["trips"].update_one(
        {"_id": id},
        {"$set": {"status": status}},
    )

    stored_trip = database["trips"].find_one({"_id": id})
    if stored_trip is not None:
        return stored_trip

    return None


def update_trip_to_next_status(id: str, mongo_client):

    database = mongo_client[DB_NAME]

    trip = database["trips"].find_one({"_id": id})

    if trip is not None:
        status = trip_status.StatusFactory(trip["status"])

        if status.name() == trip_status.DriverAssigned().name():
            database["trips"].update_one(
                {"_id": id},
                {
                    "$set": {
                        "status": status.next().name(),
                        "start": datetime.datetime.now(),
                    }
                },
            )
        elif status == trip_status.InProgress():
            database["trips"].update_one(
                {"_id": id},
                {
                    "$set": {
                        "status": status.next().name(),
                        "finish": datetime.datetime.now(),
                    }
                },
            )
        else:
            database["trips"].update_one(
                {"_id": id},
                {"$set": {"status": status.next().name()}},
            )

    stored_trip = database["trips"].find_one({"_id": id})
    if stored_trip is not None:
        return stored_trip

    return None


def cancel_trip(id: str, mongo_client):

    database = mongo_client[DB_NAME]

    trip = database["trips"].find_one({"_id": id})
    if trip is not None:
        status = trip_status.StatusFactory(trip["status"])
        database["trips"].update_one(
            {"_id": id},
            {"$set": {"status": status.cancel().name()}},
        )
        # TO-DO

    stored_trip = database["trips"].find_one({"_id": id})

    if stored_trip is not None:
        return stored_trip

    return None

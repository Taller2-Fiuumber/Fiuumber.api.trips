from src.utils.notifications_processor import (
    notify_for_assigned_driver,
    notify_for_new_trip,
)

from src.utils.payments_processor import create_trip_payments, process_payment

import src.domain.status as trip_status
import datetime


from os import environ

DB_NAME = environ["DB_NAME"] if "DB_NAME" in environ else "Fiuumber"


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

    if status == trip_status.Terminated().name():
        try:
            (passenger_payment, driver_payment) = create_trip_payments(mongo_client, id)
            process_payment(passenger_payment)
            process_payment(driver_payment)
        except Exception as ex:
            print(
                f"[ERROR -> Continue] cannot create or process payments for trip {id} reason: {str(ex)}"
            )
            pass

    if status == trip_status.DriverAssigned().name():
        try:
            notify_for_assigned_driver(mongo_client, id)
        except Exception as ex:
            print(
                f"[ERROR -> Continue] send notification for driver assigned {id} reason: {str(ex)}"
            )
            pass

    if status == trip_status.Requested().name():
        try:
            notify_for_new_trip(id)
        except Exception as ex:
            print(
                f"[ERROR -> Continue] send notification for trip requested {id} reason: {str(ex)}"
            )
            pass

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

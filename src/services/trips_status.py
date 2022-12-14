from fastapi import APIRouter, Body, Request, HTTPException, status
from pymongo import MongoClient
from src.utils.notifications_processor import notify_for_assigned_driver, notify_for_new_trip

from src.utils.payments_processor import create_trip_payments, process_payment

import src.domain.status as trip_status
import datetime

from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

router = APIRouter()


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
        status = body.get("status")

        database["trips"].update_one(
            {"_id": id},
            {"$set": {"status": status}},
        )

        if status == trip_status.Terminated().name():
            try:
                (passenger_payment, driver_payment) = create_trip_payments(id)
                process_payment(passenger_payment)
                process_payment(driver_payment)
            except Exception as ex:
                print(
                    f"[ERROR -> Continue] cannot create or process payments for trip {id} reason: {str(ex)}"
                )
                pass

        if status == trip_status.DriverAssigned().name():
            try:
                notify_for_assigned_driver(id)
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

        return stored_trip

    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Error updating status {id} trip: {str(ex)}"
        )


@router.put("/trip/{id}/status/next", response_description="Update a trip status")
def update_trip_to_next_status(id: str, request: Request, body=Body(...)):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]

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

        return stored_trip

    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Error updating status {id} trip: {str(ex)}"
        )


@router.put("/trip/{id}/status/cancel", response_description="Update a trip status")
def cancel_trip(id: str, request: Request, body=Body(...)):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]

        trip = database["trips"].find_one({"_id": id})
        if trip is not None:
            status = trip_status.StatusFactory(trip["status"])
            database["trips"].update_one(
                {"_id": id},
                {"$set": {"status": status.cancel()}},
            )
            # TO-DO

        stored_trip = database["trips"].find_one({"_id": id})

        return stored_trip

    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Error updating status {id} trip: {str(ex)}"
        )

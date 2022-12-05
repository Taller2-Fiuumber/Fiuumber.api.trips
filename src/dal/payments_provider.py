from pymongo import MongoClient
import datetime
from os import environ

from fastapi.encoders import jsonable_encoder
from src.domain.payment import Payment

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]
MAX_ETH_TEST = 0.00000001

mongo_client = MongoClient(MONGODB_URL, connect=False)
database = mongo_client.mongodb_client[DB_NAME]


def get_pending_payments():
    processing_date = datetime.datetime.now() - datetime.timedelta(seconds=20)
    # Traigo los payments que no se hayan procesado y que no se estén procesando
    # o bien se hayan colgado procesando
    pending_payments = database["payments"].find(
        {
            "$and": [
                {"processedAt": None},
                {
                    "$or": [
                        {"startedProcessing": None},
                        {"startedProcessing": {"$lte": processing_date}},
                    ]
                },
            ]
        }
    )
    return list(pending_payments)


def create_payment(payment: Payment):
    if payment.ammount > MAX_ETH_TEST:
        raise Exception("ETH value provided is too large for testing purposes")
    try:
        payment = jsonable_encoder(payment)

        existing_payment = database["payments"].find_one(
            {"$and": [{"tripId": payment["tripId"]}, {"type": payment["type"]}]}
        )

        if existing_payment is not None:
            raise Exception(
                f'Cannot create another {payment["type"]} payment for this trip'
            )

        new_payment = database["payments"].insert_one(payment)
        created_payment = database["payments"].find_one(
            {"_id": new_payment.inserted_id}
        )
        return created_payment
    except Exception as ex:
        print("[ERROR] Error in create_payment: " + str(ex))
        raise ex


def get_incomplete_payments():
    try:
        payments = database["payments"].aggregate(
            [
                {
                    "$group": {
                        "_id": {"tripId": "$tripId"},
                        "count": {"$sum": 1},
                        "data": {"$addToSet": "$$ROOT"},
                    },
                },
                {"$match": {"count": {"$eq": 1}}},
            ]
        )
        return list(payments)
    except Exception as ex:
        print("[ERROR] Error in get_all_payments: " + str(ex))
        raise ex


def get_all_payments():
    try:
        # database["payments"].delete_many({})
        payments = database["payments"].find()
        return list(payments)
    except Exception as ex:
        print("[ERROR] Error in get_all_payments: " + str(ex))
        raise ex


def mark_payment_as_processing(id: str):
    try:
        database["payments"].update_one(
            {"_id": id},
            {"$set": {"startedProcessing": datetime.datetime.now()}},
        )
    except Exception as ex:
        print("[ERROR] Error in mark_payment_as_processing: " + str(ex))
        raise ex


def mark_payment_as_processed(id: str, hash: str):
    try:
        database["payments"].update_one(
            {"_id": id},
            {"$set": {"processedAt": datetime.datetime.now(), "hash": hash}},
        )
    except Exception as ex:
        print("[ERROR] Error in mark_payment_as_processing: " + str(ex))
        raise ex

from datetime import datetime, timedelta
from os import environ

from fastapi.encoders import jsonable_encoder

DB_NAME = environ["DB_NAME"] if "DB_NAME" in environ else "Fiuumber"
MAX_ETH_TEST = 0.0005


def get_pending_payments(mongo_client):
    database = mongo_client[DB_NAME]

    processing_date = datetime.now() - timedelta(seconds=20)
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


def create_payment(payment, mongo_client):
    database = mongo_client[DB_NAME]

    try:
        payment = jsonable_encoder(payment)
        if payment["amount"] > MAX_ETH_TEST:
            raise Exception("ETH value provided is too large for testing purposes")

        existing_payment = database["payments"].find_one(
            {"$and": [{"tripId": payment["tripId"]}, {"type": payment["type"]}]}
        )

        if payment["tripId"] is not None and existing_payment is not None:
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


def get_incomplete_payments(mongo_client):
    try:
        database = mongo_client[DB_NAME]
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


def get_all_payments(mongo_client):
    try:
        database = mongo_client[DB_NAME]
        # database["payments"].delete_many({})
        payments = database["payments"].find()
        return list(payments)
    except Exception as ex:
        print("[ERROR] Error in get_all_payments: " + str(ex))
        raise ex


def mark_payment_as_processing(id: str, mongo_client):
    try:
        database = mongo_client[DB_NAME]
        database["payments"].update_one(
            {"_id": id},
            {"$set": {"startedProcessing": datetime.now()}},
        )
        return database["payments"].find_one({"_id": id})
    except Exception as ex:
        print("[ERROR] Error in mark_payment_as_processing: " + str(ex))
        raise ex


def mark_payment_as_processed(id: str, hash: str, mongo_client):
    try:
        database = mongo_client[DB_NAME]
        database["payments"].update_one(
            {"_id": id},
            {"$set": {"processedAt": datetime.now(), "hash": hash}},
        )
        return database["payments"].find_one({"_id": id})
    except Exception as ex:
        print("[ERROR] Error in mark_payment_as_processing: " + str(ex))
        raise ex

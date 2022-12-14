import mongomock
from fastapi.encoders import jsonable_encoder
from src.domain.payment import Payment
import src.services.payments as services
from datetime import datetime

from os import environ

DB_NAME = environ["DB_NAME"] if "DB_NAME" in environ else "Fiuumber"


class TestPaymentsService:
    def setUp(self):
        external_data_1 = {
            "id": "1",
            "tripId": "ddfdsfsdf-b04a-4b30-b4sdf6c-fsdtjkjj",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "amount": 0.00000001,
            "tx_hash": "0x030d20dab0b53c123a12f2696a5c8bd23f449789d677a1571e1cdea6eacf0285",
            "type": "TO_RECEIVER",
            "wallet_address": "",
            "order": 1,
        }
        payment_1 = Payment(**external_data_1)

        self.payment_1 = jsonable_encoder(payment_1)

        external_data_2 = {
            "id": "2",
            "tripId": "ddfdsfsdf-b04a-4b30-b4sdf6c-fsdtjkjj",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "processedAt": datetime.now(),
            "startedProcessing": datetime.now(),
            "amount": 0.00000001,
            "tx_hash": "0x030d20dab0b53c123a12f2696a5c8bd23f449789d677a1571e1cdea6eacf0285",
            "type": "TO_SENDER",
            "wallet_address": "",
            "order": 1,
        }
        payment_2 = Payment(**external_data_2)
        self.payment_2 = jsonable_encoder(payment_2)

        external_data_3 = {
            "id": "3",
            "tripId": "ddfdsfsdf-b04a-4b30-b4sdf6c-fsdtjkjj",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "amount": 0.00000001,
            "tx_hash": "0x030d20dab0b53c123a12f2696a5c8bd23f449789d677a1571e1cdea6eacf0285",
            "type": "TO_RECEIVER",
            "wallet_address": "",
            "order": 1,
        }
        payment_3 = Payment(**external_data_3)
        self.payment_3 = jsonable_encoder(payment_3)

    def test_get_trip_fare_final_is_none(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["payments"].insert_one(self.payment_1)
        mongo_client[DB_NAME]["payments"].insert_one(self.payment_2)

        assert services.get_all_payments(mongo_client) == [
            self.payment_1,
            self.payment_2,
        ]

    def test_get_pending_payment(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["payments"].insert_one(self.payment_1)
        mongo_client[DB_NAME]["payments"].insert_one(self.payment_2)

        assert services.get_pending_payments(mongo_client) == [self.payment_1]

    def test_create_payment(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        assert services.create_payment(self.payment_3, mongo_client) == self.payment_3

    def test_get_incomplete_payments(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["payments"].insert_one(self.payment_1)
        mongo_client[DB_NAME]["payments"].insert_one(self.payment_2)

        assert services.get_incomplete_payments(mongo_client) == []

    def test_mark_payment_as_processing(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["payments"].insert_one(self.payment_1)

        assert (
            services.mark_payment_as_processing(self.payment_1["_id"], mongo_client)[
                "startedProcessing"
            ]
            is not None
        )

    def test_mark_payment_as_processed(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["payments"].insert_one(self.payment_1)

        assert (
            services.mark_payment_as_processed(
                self.payment_1["_id"], self.payment_1["tx_hash"], mongo_client
            )["processedAt"]
            is not None
        )

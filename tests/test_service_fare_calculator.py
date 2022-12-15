import mongomock
from fastapi.encoders import jsonable_encoder
from src.domain.trip import Trip
import src.services.fare_calculator as service
from datetime import datetime


from os import environ

DB_NAME = environ["DB_NAME"] if "DB_NAME" in environ else "fiuumber"


class TestFareCalculatorService:
    def setUp(self):
        external_data_3 = {
            "id": "1",
            "passengerId": "10",
            "driverId": "50",
            "from_latitude": -34.603683,
            "from_longitude": -58.381557,
            "to_latitude": -34.6175841,
            "to_longitude": -58.3682286,
            "subscription": "REGULAR",
            "status": "TERMINATED",
            "finalPrice": 500,
            "from_address": "Calle Falsa 123",
            "to_address": "Calle Falsa 666",
            "start": datetime.now(),
            "finish": datetime.now(),
        }
        trip1 = Trip(**external_data_3)
        self.trip1 = jsonable_encoder(trip1)

    def test_calculate(self):
        assert (
            service.calculate(-39.603683, -31.6175841, -50.381557, -55.3682286)
            == 40067.74
        )

    def test_calculate_final(self):
        assert (
            service.calculate_final(
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1, 8, 9, 2, 3, 4, 5
            )
            == 374
        )

    def test_calculate_test(self):
        assert (
            service.calculate_test(
                1, 1, 2, 3, 4, 5, 1, 1, 2, 3, 4, 50, 1, 2, 3, 1, 0, 9, 8, 9, 1
            )
            == 132
        )

    def test_lineal(self):
        assert (
            service.lineal(-39.603683, -31.6175841, -50.381557, -55.3682286) == 0.013982
        )

    def test_daily_trip_amount_driver(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        assert service.daily_trip_amount_driver(mongo_client, "50") == 0

    def test_daily_trip_amount_passenger(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        assert service.daily_trip_amount_passenger(mongo_client, "10") == 0

    def test_monthly_trip_amount_driver(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        assert service.monthly_trip_amount_driver(mongo_client, "50") == 0

    def test_monthly_trip_amount_passenger(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        assert service.monthly_trip_amount_passenger(mongo_client, "10") == 0

    # def test_get_driver_seniority(self):
    #     self.setUp()
    #     mongo_client = mongomock.MongoClient()
    #     mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
    #     assert service.get_driver_seniority(mongo_client, "50") == 0

    # def test_get_passenger_seniority(self):
    #     self.setUp()
    #     mongo_client = mongomock.MongoClient()
    #     mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
    #     assert service.get_passenger_seniority(mongo_client, "10") == 0

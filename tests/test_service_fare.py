import mongomock
from fastapi.encoders import jsonable_encoder
from src.domain.fare_rule import FareRule
from src.domain.trip import Trip
import src.services.fare as service
from datetime import datetime


from os import environ

DB_NAME = environ["DB_NAME"] if "DB_NAME" in environ else "Fiuumber"


class TestFareService:
    def setUp(self):
        external_data_1 = {
            "_id": "1",
            "selected": True,
            "createdAt": datetime(2022, 9, 9, 2),
            "updatedAt": datetime(2022, 9, 9, 2),
            "minimum": 200.0,
            "duration": 5,
            "distance": 6,
            "dailyTripAmountDriver": 0.7,
            "dailyTripAmountPassenger": -0.7,
            "monthlyTripAmountDriver": 0.8,
            "monthlyTripAmountPassenger": -0.8,
            "seniorityDriver": 0.5,
            "seniorityPassenger": -0.25,
            "recentTripAmount": -0.2,
            "nightShift": 0,
        }
        fare_rule1 = FareRule(**external_data_1)

        self.fare_rule1 = jsonable_encoder(fare_rule1)

        external_data_1 = {
            "_id": "2",
            "selected": False,
            "createdAt": datetime(2022, 9, 9, 2),
            "updatedAt": datetime(2022, 9, 9, 2),
            "minimum": 200.0,
            "duration": 5,
            "distance": 6,
            "dailyTripAmountDriver": 0.7,
            "dailyTripAmountPassenger": -0.7,
            "monthlyTripAmountDriver": 0.8,
            "monthlyTripAmountPassenger": -0.8,
            "seniorityDriver": 0.5,
            "seniorityPassenger": -0.25,
            "recentTripAmount": -0.2,
            "nightShift": 0,
        }
        fare_rule2 = FareRule(**external_data_1)
        self.fare_rule2 = jsonable_encoder(fare_rule2)

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

    def test_get_trip_fare(self):
        mongo_client = mongomock.MongoClient()
        print(
            service.get_trip_fare(
                mongo_client, -39.603683, -31.6175841, -50.381557, -55.3682286
            )
        )
        assert (
            service.get_trip_fare(
                mongo_client, -39.603683, -31.6175841, -50.381557, -55.3682286
            )
            is None
        )

    def test_get_trip_fare_final_is_none(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        assert service.get_trip_fare_to_test_fare_rule(mongo_client) is None

    def test_get_trip_fare_to_test_fare_rule(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["fare_rules"].insert_one(self.fare_rule1)
        assert (
            round(service.get_trip_fare_to_test_fare_rule(mongo_client, "1"), 2)
            == 457.45
        )

    def test_get_trip_fare_to_test_new_fare_rule(self):
        self.setUp()
        assert round(service.get_trip_fare_to_test_new_fare_rule(), 2) == 225.15

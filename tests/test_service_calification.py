import mongomock
from fastapi.encoders import jsonable_encoder
from src.domain.calification import Calification
import src.services.calification as service
from datetime import datetime


# DB_NAME = environ["DB_NAME"]
DB_NAME = "Fiuumber"


class TestCalification:
    def setUp(self):
        external_data_1 = {
            "_id": "1",
            "passengerId": "5",
            "driverId": "6",
            "tripId": "100",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "stars": 3,
            "comments": "Nice driver. Love the scene.",
            "reviewer": "PASSENGER",
        }
        calification1 = Calification(**external_data_1)

        external_data_2 = {
            "_id": "2",
            "passengerId": "3",
            "driverId": "4",
            "tripId": "101",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "stars": 1,
            "comments": "Nice driver",
            "reviewer": "DRIVER",
        }
        calification2 = Calification(**external_data_2)

        external_data_3 = {
            "_id": "3",
            "passengerId": "5",
            "driverId": "6",
            "tripId": "105",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "stars": 5,
            "comments": "Nice driver. Love the scene.",
            "reviewer": "PASSENGER",
        }
        calification3 = Calification(**external_data_3)

        external_data_4 = {
            "_id": "4",
            "passengerId": "3",
            "driverId": "4",
            "tripId": "103",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "stars": 3,
            "comments": "Nice driver",
            "reviewer": "DRIVER",
        }
        calification4 = Calification(**external_data_4)

        self.calification1 = jsonable_encoder(calification1)
        self.calification2 = jsonable_encoder(calification2)
        self.calification3 = jsonable_encoder(calification3)
        self.calification4 = jsonable_encoder(calification4)

    def test_create_calification(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        result = self.calification1
        result["_id"] = 1
        assert (
            service.create_calification_passenger(mongo_client, self.calification1)
            == result
        )

    def test_find_califications(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification1)
        result = self.calification1
        result["_id"] = "1"
        assert service.find_califications(0, 1, mongo_client) == [result]

    def test_find_califications_passenger(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification1)
        result = self.calification1
        result["_id"] = "1"
        assert service.find_califications_of_passenger(0, 10, mongo_client) == [result]

    def test_find_califications_driver(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification2)
        result = self.calification2
        result["_id"] = "2"
        assert service.find_califications_of_driver(0, 1, mongo_client) == [result]

    def test_find_califications_of_passenger_by_trip_id(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification1)
        result = self.calification1
        result["_id"] = "1"
        assert service.find_califications_of_passenger_by_tripId(
            "100", 0, 1, mongo_client
        ) == [result]

    def test_find_califications_of_driver_by_trip_id(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification2)
        result = self.calification2
        result["_id"] = "2"
        assert service.find_califications_of_driver_by_tripId(
            "101", 0, 1, mongo_client
        ) == [result]

    def test_find_califications_of_passenger_by_tripId_and_by_passengerId(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification1)
        result = self.calification1
        result["_id"] = "1"
        assert service.find_califications_of_passenger_by_tripId_and_by_passengerId(
            "5", "100", 0, 1, mongo_client
        ) == [result]

    def find_califications_of_driver_by_tripId_and_by_driverId(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification2)
        result = self.calification2
        result["_id"] = "2"
        assert service.find_califications_of_driver_by_tripId_and_by_driverId(
            "4", "100", 0, 1, mongo_client
        ) == [result]

    def test_find_califications_of_passenger_by_passengerId(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification2)
        result = self.calification2
        result["_id"] = "2"
        assert service.find_califications_of_passenger_by_passengerId(
            "3", 0, 1, mongo_client
        ) == [result]

    def test_find_califications_of_driver_by_driverId(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification1)
        result = self.calification1
        result["_id"] = "1"
        assert service.find_califications_of_driver_by_driverId(
            "6", 0, 1, mongo_client
        ) == [result]

    def test_find_califications_mean_of_driver_by_driverId(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification1)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification3)
        assert (
            service.find_califications_mean_of_driver_by_driverId("6", mongo_client)
            == 4
        )

    def test_find_califications_mean_of_driver_by_passengerId(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification2)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification4)
        assert (
            service.find_califications_mean_of_driver_by_passengerId("3", mongo_client)
            == 2
        )

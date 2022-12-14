import mongomock
from fastapi.encoders import jsonable_encoder
from src.domain.calification import Calification
import src.services.calification_metrics as service
from datetime import datetime


# DB_NAME = environ["DB_NAME"]
DB_NAME = "Fiuumber"


class TestCalificationMetrics:
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

    def test_get_calification_passenger_min(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification1)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification2)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification3)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification4)
        assert service.get_calification_passenger_min(mongo_client) == 1

    def test_get_calification_passenger_max(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification1)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification2)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification3)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification4)
        assert service.get_calification_passenger_max(mongo_client) == 3

    def test_get_calification_passenger_avg(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification1)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification2)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification3)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification4)
        assert service.get_calification_passenger_avg(mongo_client) == 2

    def test_get_calification_driver_min(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification1)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification2)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification3)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification4)
        assert service.get_calification_driver_min(mongo_client) == 3

    def test_get_calification_driver_max(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification1)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification2)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification3)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification4)
        assert service.get_calification_driver_max(mongo_client) == 5

    def test_get_calification_driver_avg(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["calification"].insert_one(self.calification1)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification2)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification3)
        mongo_client[DB_NAME]["calification"].insert_one(self.calification4)
        assert service.get_calification_driver_avg(mongo_client) == 4

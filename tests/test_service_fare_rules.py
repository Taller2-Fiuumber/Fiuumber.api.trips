import mongomock
from fastapi.encoders import jsonable_encoder
from src.domain.fare_rule import FareRule
import src.services.fare_rules as service
from datetime import datetime

from os import environ

DB_NAME = environ["DB_NAME"] if "DB_NAME" in environ else "fiuumber"


class TestFareRulesService:
    def setUp(self):
        external_data_1 = {
            "time": 1,
            "_id": "1",
            "selected": True,
            "createdAt": datetime(2022, 9, 9, 2),
            "updatedAt": datetime(2022, 9, 9, 2),
            "minimum": 200.0,
            "duration": 5,
            "distance": 6,
            "dailyTripAmountDriver": 0.7,
            "dailyTripAmountPassenger": -0.7,
            "monthlyTripAmountDrive": 0.8,
            "monthlyTripAmountPassenger": -0.8,
            "seniorityDriver": 0.5,
            "seniorityPassenger": -0.25,
            "recentTripAmount": -0.2,
        }
        fare_rule1 = FareRule(**external_data_1)
        self.fare_rule1 = jsonable_encoder(fare_rule1)

        external_data_1 = {
            "time": 1,
            "_id": "2",
            "selected": False,
            "createdAt": datetime(2022, 9, 9, 2),
            "updatedAt": datetime(2022, 9, 9, 2),
            "minimum": 200.0,
            "duration": 5,
            "distance": 6,
            "dailyTripAmountDriver": 0.7,
            "dailyTripAmountPassenger": -0.7,
            "monthlyTripAmountDrive": 0.8,
            "monthlyTripAmountPassenger": -0.8,
            "seniorityDriver": 0.5,
            "seniorityPassenger": -0.25,
            "recentTripAmount": -0.2,
        }
        fare_rule2 = FareRule(**external_data_1)
        self.fare_rule2 = jsonable_encoder(fare_rule2)

    def test_get_selected_fare(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["fare_rules"].insert_one(self.fare_rule1)
        assert service.get_selected_fare(mongo_client) == self.fare_rule1

    def test_create_fare_rule(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        assert (
            service.create_fare_rule(mongo_client, self.fare_rule1) == self.fare_rule1
        )

    def test_list_fare_rule(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["fare_rules"].insert_one(self.fare_rule1)
        mongo_client[DB_NAME]["fare_rules"].insert_one(self.fare_rule2)
        assert service.list_fare_rules(mongo_client) == [
            self.fare_rule1,
            self.fare_rule2,
        ]

    def test_find_fare_rule_by_id(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["fare_rules"].insert_one(self.fare_rule1)
        mongo_client[DB_NAME]["fare_rules"].insert_one(self.fare_rule2)
        assert service.find_fare_rules_by_id("1", mongo_client) == self.fare_rule1

    def test_select_a_fare_rule(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["fare_rules"].insert_one(self.fare_rule2)
        result = self.fare_rule2
        result["selected"] = True
        assert service.select_a_fare_rule("2", mongo_client) == self.fare_rule2

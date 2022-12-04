import uuid
from pydantic import BaseModel, Field
import datetime
from pymongo import MongoClient
from typing import Optional
import geopy.distance
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

class Trip(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    passengerId: str = Field(...)
    driverId: str = Field(...)
    from_latitude: float = Field(...)
    from_longitude: float = Field(...)
    to_latitude: float = Field(...)
    to_longitude: float = Field(...)
    start: Optional[datetime] = None
    finish: Optional[datetime] = None
    subscription: str = Field(...)
    status: str = Field(...)
    finalPrice: float = Field(...)
    from_address: str = Field(...)
    to_address: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "passengerId": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "driverId": "2320930329-b04a-4b30-b46c-fsdfwefwefw",
                "from_latitude": -34.603683,
                "from_longitude": -58.381557,
                "to_latitude": -34.6175841,
                "to_longitude": -58.3682286,
                "subscription": "REGULAR",
                "status": "REQUESTED",
                "finalPrice": 532.50,
                "from_address": "Calle Falsa 123",
                "to_address": "Calle Falsa 666",
            }
        }
        orm_mode = True


class TripUpdate(BaseModel):
    passengerId: str = Field(...)
    driverId: str = Field(...)
    from_latitude: float = Field(...)
    from_longitude: float = Field(...)
    to_latitude: float = Field(...)
    to_longitude: float = Field(...)
    start: Optional[datetime] = None
    finish: Optional[datetime] = None
    subscription: str = Field(...)
    status: str = Field(...)
    finalPrice: float = Field(...)
    from_address: str = Field(...)
    to_address: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "passengerId": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "driverId": "2320930329-b04a-4b30-b46c-fsdfwefwefw",
                "from_latitude": -34.603683,
                "from_longitude": -58.381557,
                "to_latitude": -34.6175841,
                "to_longitude": -58.3682286,
                "to_location": "Don Quixote",
                "subscription": "VIP",
                "status": "Done",
                "finalPrice": 532.50,
                "from_address": "Calle Falsa 123",
                "to_address": "Calle Falsa 666",
            }
        }
        orm_mode = True

    def duration(self):
        return self.end - self.start

    def distance_in_km(self):
        coords_1 = (self.to_latitude, self.to_longitude)
        coords_2 = (self.from_latitude, self.from_longitude)
        return geopy.distance.geodesic(coords_1, coords_2).km

    def daily_trip_amount_driver(self):
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]

        stage_match_driver = {"$match": {"driverId": self.driverId}}
        stage_match_today_trips = {"$match": {
                "$gte": datetime.today(),
                "$lte": datetime.today() + datetime.timedelta(days=1)
            }
        }
        stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
        pipeline = [stage_match_driver, stage_match_today_trips, stage_trip_count]

        data = database["trips"].aggregate(pipeline)
        if (data == None):
            return 0
        return list(data)[0]["count"]

    def daily_trip_amount_passenger(self):
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]

        stage_match_passenger = {"$match": {"passengerId": self.passengerId}}
        stage_match_today_trips = {"$match": {
                "$gte": datetime.today(),
                "$lte": datetime.today() + datetime.timedelta(days=1)
            }
        }
        stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
        pipeline = [stage_match_passenger, stage_match_today_trips, stage_trip_count]

        data = database["trips"].aggregate(pipeline)
        if (data == None):
            return 0
        return list(data)[0]["count"]

    def monthly_trip_amount_driver(self):
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]

        stage_match_driver = {"$match": {"driverId": self.driverId}}
        stage_match_monthly_trips = {"$match": {
                "$gte": datetime.today().replace(day=1),
                "$lte": datetime.today() + relativedelta(day=31)
            }
        }
        stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
        pipeline = [stage_match_driver, stage_match_monthly_trips, stage_trip_count]

        data = database["trips"].aggregate(pipeline)
        if (data == None):
            return 0
        return list(data)[0]["count"]

    def monthly_trip_amount_passenger(self):
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]

        stage_match_passenger = {"$match": {"passengerId": self.passengerId}}
        stage_match_monthly_trips = {"$match": {
                "$gte": datetime.today().replace(day=1),
                "$lte": datetime.today() + relativedelta(day=31)
            }
        }
        stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
        pipeline = [stage_match_passenger, stage_match_monthly_trips, stage_trip_count]

        data = database["trips"].aggregate(pipeline)
        if (data == None):
            return 0
        return list(data)[0]["count"]

    def get_driver_seniority(self):
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]

        stage_match_driver = {"$match": {"driverId": self.driverId}}
        stage_sort_trip = {'$sort': {'start': 1}}
        stage_first_trip = {'_id': None, 'first': {'$first': '$start'}}

        pipeline = [stage_match_driver, stage_sort_trip, stage_first_trip]

        data = database["trips"].aggregate(pipeline)
        if (data == None):
            return None
        return list(data)

    def get_passenger_seniority(self):
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]

        stage_match_passenger = {"$match": {"passengerId": self.passengerId}}
        stage_sort_trip = {'$sort': {'start': 1}}
        stage_first_trip = {'_id': None, 'first': {'$first': '$start'}}

        pipeline = [stage_match_driver, stage_sort_trip, stage_first_trip]

        data = database["trips"].aggregate(pipeline)
        if (data == None):
            return None
        return list(data)

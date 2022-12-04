import uuid
from pydantic import BaseModel, Field
import datetime
from pymongo import MongoClient
from typing import Optional

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
    start: Optional[datetime.datetime] = None
    finish: Optional[datetime.datetime] = None
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
    start: Optional[datetime.datetime] = None
    finish: Optional[datetime.datetime] = None
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

    def get_driver_trips_in_day(self):
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]
        stage_group_year = {
            "$group": {
                    "_id": "$year",
                    # Count the number of movies in the group:
                    "movie_count": { "$sum": 1 },
            }
        }

        trips = database["trips"].findall({"driverId": self.driverId, "start": datetime.datetime.today()})
        if (trips == None):
            return 0
        return len(trips)

    def get_driver_trips_in_month(self):
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]
        trips = database["trips"].findall({"driverId": self.driverId, "start": datetime.datetime.today()})
        if (trips == None):
            return 0
        return len(trips)

    def get_passenger_trips_in_day(self):
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]
        trips = database["trips"].findall({"passengerId": self.passengerId, "start": datetime.datetime.today()})
        if (trips == None):
            return 0
        return len(trips)

    def get_passenger_trips_in_month(self):
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]
        trips = database["trips"].findall({"passengerId": self.passengerId, "start": datetime.datetime.today()})
        if (trips == None):
            return 0
        return len(trips)

    def get_driver_seniority(self):
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]
        pipeline = [
            {"$unwind": "$tags"},
            {"$group": {"driverId": "$tags", "min": {"$sum": 1}}},
        ]
        trips = database["trips"].find({"driverId": self.driverId}).aggregate(pipeline)
        if (trips == None):
            return 0
        return len(trips)

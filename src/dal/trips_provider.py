from pymongo import MongoClient
from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

mongo_client = MongoClient(MONGODB_URL, connect=False)
database = mongo_client.mongodb_client[DB_NAME]


def get_trip_by_id(trip_id):
    trip = database["trips"].find_one({"_id": trip_id})
    return trip

from math import radians, cos, sin, asin, sqrt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from pymongo import MongoClient

from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

def calculate(from_latitude, to_latitude, from_longitude, to_longitude):
    distance_km = __distance(from_latitude, to_latitude, from_longitude, to_longitude)
    base_price = 250  # TODO add to database
    price_per_km = 40  # TODO add to database
    return round(base_price + (distance_km * price_per_km), 2)

def calculate_final(
    minimum_fare,
    duration_fare,
    distance_fare,
    dailyTripAmountDriver_fare,
    dailyTripAmountPassenger_fare,
    monthlyTripAmountDrive_fare,
    monthlyTripAmountPassenger_fare,
    seniorityDriver_fare,
    seniorityPassenger_fare,
    recentTripAmount_fare,
    duration,
    distance,
    dailyTripAmountDriver,
    dailyTripAmountPassenger,
    monthlyTripAmountDrive,
    monthlyTripAmountPassenger,
    seniorityDriver,
    seniorityPassenger,
    recentTripAmount,
):

    return (
        minimum_fare
        + duration_fare * duration
        + distance_fare * distance
        + dailyTripAmountDriver_fare * dailyTripAmountDriver
        + dailyTripAmountPassenger_fare * dailyTripAmountPassenger
        + monthlyTripAmountDrive_fare * monthlyTripAmountDrive
        + monthlyTripAmountPassenger_fare * monthlyTripAmountPassenger
        + seniorityDriver_fare * seniorityDriver
        + seniorityPassenger_fare * seniorityPassenger
        + recentTripAmount_fare * recentTripAmount
    )

def calculate_test(
    minimum_fare,
    duration_fare,
    distance_fare,
    dailyTripAmountDriver_fare,
    dailyTripAmountPassenger_fare,
    monthlyTripAmountDrive_fare,
    monthlyTripAmountPassenger_fare,
    seniorityDriver_fare,
    seniorityPassenger_fare,
    recentTripAmount_fare,
    duration,
    distance,
    dailyTripAmountDriver,
    dailyTripAmountPassenger,
    monthlyTripAmountDrive,
    monthlyTripAmountPassenger,
    seniorityDriver,
    seniorityPassenger,
    recentTripAmount,
):

    return (
        minimum_fare
        + duration_fare * duration
        + distance_fare * distance
        + dailyTripAmountDriver_fare * dailyTripAmountDriver
        + dailyTripAmountPassenger_fare * dailyTripAmountPassenger
        + monthlyTripAmountDrive_fare * monthlyTripAmountDrive
        + monthlyTripAmountPassenger_fare * monthlyTripAmountPassenger
        + seniorityDriver_fare * seniorityDriver
        + seniorityPassenger_fare * seniorityPassenger
        + recentTripAmount_fare * recentTripAmount
    )


def lineal(from_latitude, to_latitude, from_longitude, to_longitude):
    # trip["from_latitude"], trip["to_latitude"], trip["from_longitude"], trip["to_longitude"]
    distance_km = __distance(from_latitude, to_latitude, from_longitude, to_longitude)
    base_price = 250  # TODO add to database
    price_per_km = 40  # TODO add to database
    return round(base_price + (distance_km * price_per_km), 2)


def __distance(lat1, lat2, lon1, lon2):

    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return c * r

def daily_trip_amount_driver(driverId):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    today =  datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    stage_match_driver = {"$match": {"driverId": driverId}}
    stage_match_today_trips = {"$match": {"start":{"$gte": today}}}
    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [stage_match_driver, stage_match_today_trips, stage_trip_count]

    data = database["trips"].aggregate(pipeline)
    if data is None:
        return 0
    return list(data)[0]['count']

def daily_trip_amount_passenger(passengerId):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    today =  datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    stage_match_passenger = {"$match": {"passengerId": passengerId}}
    stage_match_today_trips = {"$match": {"start":{"$gte": today}}}
    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [stage_match_passenger, stage_match_today_trips, stage_trip_count]

    data = database["trips"].aggregate(pipeline)
    if data is None:
        return 0
    return list(data)[0]["count"]

def monthly_trip_amount_driver(driverId):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    stage_match_driver = {"$match": {"driverId": driverId}}
    stage_match_monthly_trips = {"$match": {"start":{
        "$gte": today.replace(day=1),
        "$lte": today + relativedelta(day=31),
    }}}
    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [stage_match_driver, stage_match_monthly_trips, stage_trip_count]

    data = database["trips"].aggregate(pipeline)
    if data is None:
        return 0
    return list(data)[0]["count"]

def monthly_trip_amount_passenger(passengerId):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    stage_match_passenger = {"$match": {"passengerId": passengerId}}
    stage_match_monthly_trips = {"$match": {"start":{
        "$gte": today.replace(day=1),
        "$lte": today + relativedelta(day=31),
    }}}
    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [stage_match_passenger, stage_match_monthly_trips, stage_trip_count]

    data = database["trips"].aggregate(pipeline)
    if data is None:
        return 0
    return list(data)[0]["count"]

def get_driver_seniority(driverId):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_driver = {"$match": {"driverId": driverId}}
    stage_sort_trip = {"$sort": {"start": 1}}

    pipeline = [stage_match_driver, stage_sort_trip]

    data = database["trips"].aggregate(pipeline)
    if data is None:
        return None
    for d in list(data):
        if d["start"] != None:
            today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            return (today-datetime.strptime(d["start"], '%Y-%m-%dT%H:%M:%S')).total_seconds()/60
    return 0

def get_passenger_seniority(passengerId):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_passenger = {"$match": {"passengerId": passengerId}}
    stage_sort_trip = {"$sort": {"start": 1}}

    pipeline = [stage_match_passenger, stage_sort_trip]

    data = database["trips"].aggregate(pipeline)
    if data is None:
        return None
    for d in list(data):
        if d["start"] != None:
            today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            return (today-datetime.strptime(d["start"], '%Y-%m-%dT%H:%M:%S')).total_seconds()/60
    return 0


def get_recent_trip_amount(passengerId):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    stage_match_passenger = {"$match": {"passengerId": passengerId}}
    stage_match_monthly_trips = {"$match": {"start":{
        "$gte": today - relativedelta(day=7),
    }}}
    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [stage_match_passenger, stage_match_monthly_trips, stage_trip_count]

    data = database["trips"].aggregate(pipeline)
    if data is None:
        return 0
    return list(data)[0]["count"]

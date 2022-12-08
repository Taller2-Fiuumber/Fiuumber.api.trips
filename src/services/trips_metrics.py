from fastapi import APIRouter, Request, HTTPException
from pymongo import MongoClient

from os import environ
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]
router = APIRouter()

# Duration----------------------------------------------------------------------


@router.get(
    "/duration/min", response_description="Get trip duration minimum in minutes"
)
def get_trip_duration_min(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_trip_duration = {
        "$project": {"duration": {"$subtract": ["$finish", "$start"]}}
    }
    stage_trip_duration_min = {
        "$group": {"_id": None, "min_duration": {"$min": "$duration"}}
    }
    pipeline = [
        stage_match_terminated_status,
        stage_trip_duration,
        stage_trip_duration_min,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["min_duration"] / 60000
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/duration/max", response_description="Get trip duration maximum in minutes"
)
def get_trip_duration_max(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_trip_duration = {
        "$project": {"duration": {"$subtract": ["$finish", "$start"]}}
    }
    stage_trip_duration_max = {
        "$group": {"_id": None, "max_duration": {"$max": "$duration"}}
    }
    pipeline = [
        stage_match_terminated_status,
        stage_trip_duration,
        stage_trip_duration_max,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["max_duration"] / 60000
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/duration/avg", response_description="Get trip duration average in minutes"
)
def get_trip_duration_avg(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_trip_duration = {
        "$project": {"duration": {"$subtract": ["$finish", "$start"]}}
    }
    stage_trip_duration_avg = {
        "$group": {"_id": None, "avg_duration": {"$avg": "$duration"}}
    }
    pipeline = [
        stage_match_terminated_status,
        stage_trip_duration,
        stage_trip_duration_avg,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["avg_duration"] / 60000
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/duration/months/range", response_description="Count new trips last n months"
)
def count_trips_duration_last_n_months_range(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_match_last_n_month = {
        "$match": {"start": {"$gte": datetime.today() - relativedelta(months=+amount)}}
    }
    stage_trip_duration = {
        "$project": {
            "duration": {"$divide": [{"$subtract": ["$finish", "$start"]}, 60000]}
        }
    }
    stage_trip_count = {"$group": {"_id": "$duration", "count": {"$sum": 1}}}
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_month,
        stage_trip_duration,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/duration/years-and-months/range",
    response_description="Count duratoin of trips last n months and years",
)
def count_trips_duration_last_n_years_and_m_months_range(
    years: int, months: int, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_match_last_n_years_month = {
        "$match": {
            "start": {
                "$gte": datetime.today() - relativedelta(years=+years, months=+months)
            }
        }
    }
    stage_trip_duration = {
        "$project": {
            "duration": {"$divide": [{"$subtract": ["$finish", "$start"]}, 60000]}
        }
    }
    stage_trip_count = {"$group": {"_id": "$duration", "count": {"$sum": 1}}}
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_years_month,
        stage_trip_duration,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/duration/years/range", response_description="Count new trips last n years"
)
def count_trips_duration_last_n_years_range(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_match_last_n_years = {
        "$match": {"start": {"$gte": datetime.today() - relativedelta(years=+amount)}}
    }
    stage_trip_duration = {
        "$project": {
            "duration": {"$divide": [{"$subtract": ["$finish", "$start"]}, 60000]}
        }
    }
    stage_trip_count = {"$group": {"_id": "$duration", "count": {"$sum": 1}}}
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_years,
        stage_trip_duration,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/duration/days/range", response_description="Count new trips last n days")
def count_trips_duration_last_n_days_range(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_match_last_n_days = {
        "$match": {"start": {"$gte": datetime.today() - timedelta(days=amount)}}
    }
    stage_trip_duration = {
        "$project": {
            "duration": {"$divide": [{"$subtract": ["$finish", "$start"]}, 60000]}
        }
    }
    stage_trip_count = {"$group": {"_id": "$duration", "count": {"$sum": 1}}}
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_days,
        stage_trip_duration,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)
    raise HTTPException(status_code=500, detail="Internal error")


# Status------------------------------------------------------------------------


@router.get("/status/count", response_description="Count trips by status")
def count_trips_by_status(status: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": status}}
    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [stage_match_terminated_status, stage_trip_count]

    data = database["trips"].aggregate(pipeline)

    try:
        if data is not None:
            return list(data)[0]["count"]
        return 0
    except Exception as ex:
        print(ex)
        return 0


@router.get(
    "/status/passenger/{id}/count", response_description="Count trips by status"
)
def count_trips_of_passenger_by_status(id: str, status: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": status, "passengerId": id}}
    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [stage_match_terminated_status, stage_trip_count]

    data = database["trips"].aggregate(pipeline)

    try:
        if data is not None:
            return list(data)[0]["count"]
        return 0
    except Exception as ex:
        print(ex)
        return 0


@router.get("/status/driver/{id}/count", response_description="Count trips by status")
def count_trips_of_driver_by_status(id: str, status: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": status, "driverId": id}}
    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [stage_match_terminated_status, stage_trip_count]

    data = database["trips"].aggregate(pipeline)

    try:
        if data is not None:
            return list(data)[0]["count"]
        return 0
    except Exception as ex:
        print(ex)
        return 0


# Count------------------------------------------------------------------------


@router.get("/count", response_description="Count trips")
def count_trips(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [stage_trip_count]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return 0 if len(data) == 0 else list(data)[0]["count"]
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/new/count/today", response_description="Count new trips by date")
def count_trips_new_count_today(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_match_today = {"$match": {"start": {"$gte": datetime.today()}}}
    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [stage_match_terminated_status, stage_match_today, stage_trip_count]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return 0 if len(data) == 0 else list(data)[0]["count"]
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/new/count/days", response_description="Count new trips last n days")
def count_trips_new_countlast_n_days(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_match_last_n_days = {
        "$match": {"start": {"$gte": datetime.today() - timedelta(days=amount)}}
    }
    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_days,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return 0 if len(data) == 0 else list(data)[0]["count"]
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/new/count/days/range", response_description="Count new trips last n days")
def count_trips_new_countlast_n_days_range(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_match_last_n_days = {
        "$match": {"start": {"$gte": datetime.today() - timedelta(days=amount)}}
    }
    stage_trip_count = {
        "$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$start"}},
            "count": {"$sum": 1},
        }
    }
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_days,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/new/count/months", response_description="Count new trips last n months")
def count_trips_new_count_last_n_months(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}

    stage_match_last_n_month = {
        "$match": {"start": {"$gte": datetime.today() - relativedelta(months=+amount)}}
    }
    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_month,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return 0 if len(data) == 0 else list(data)[0]["count"]
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/new/count/months/range", response_description="Count new trips last n months"
)
def count_trips_new_count_last_n_months_range(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}

    stage_match_last_n_month = {
        "$match": {"start": {"$gte": datetime.today() - relativedelta(months=+amount)}}
    }
    stage_trip_count = {
        "$group": {
            "_id": {"$dateToString": {"format": "%m", "date": "$start"}},
            "count": {"$sum": 1},
        }
    }
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_month,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/new/count/years/range", response_description="Count new trips last n years"
)
def count_trips_new_count_last_n_years_range(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}

    stage_match_last_n_month = {
        "$match": {"start": {"$gte": datetime.today() - relativedelta(years=+amount)}}
    }
    stage_trip_count = {
        "$group": {
            "_id": {"$dateToString": {"format": "%Y", "date": "$start"}},
            "count": {"$sum": 1},
        }
    }
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_month,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/new/count/years-and-months/range",
    response_description="Count new trips last n years",
)
def count_trips_new_count_last_n_years_and_m_months_range(
    years: int, months: int, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}

    stage_match_last_n_month = {
        "$match": {
            "start": {
                "$gte": datetime.today() - relativedelta(years=+years, months=+months)
            }
        }
    }
    stage_trip_count = {
        "$group": {
            "_id": {"$dateToString": {"format": "%m-%Y", "date": "$start"}},
            "count": {"$sum": 1},
        }
    }
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_month,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/new/count/year", response_description="Count new trips last n years")
def count_trips_new_count_last_n_years(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}

    stage_match_last_n_month = {
        "$match": {"start": {"$gte": datetime.today() - relativedelta(years=+amount)}}
    }
    stage_trip_count = {"$group": {"_id": None, "count": {"$count": {}}}}
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_month,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return 0 if len(data) == 0 else list(data)[0]["count"]
    raise HTTPException(status_code=500, detail="Internal error")

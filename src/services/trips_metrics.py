from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# DB_NAME = environ["DB_NAME"]
DB_NAME = "Fiuumber"


# Duration----------------------------------------------------------------------


def get_trip_duration_min(mongo_client):
    database = mongo_client[DB_NAME]

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
    return None


def get_trip_duration_max(mongo_client):
    database = mongo_client[DB_NAME]

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
    return None


def get_trip_duration_avg(mongo_client):
    database = mongo_client[DB_NAME]

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
    return None


def count_trips_duration_last_n_months_range(amount: int, mongo_client): 
    database = mongo_client[DB_NAME]

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
    return None


def count_trips_duration_last_n_years_and_m_months_range(
    years: int, months: int, mongo_client
):
    database = mongo_client[DB_NAME]

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
    return None


def count_trips_duration_last_n_years_range(amount: int, mongo_client):
    database = mongo_client[DB_NAME]

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
    return None


def count_trips_duration_last_n_days_range(amount: int, mongo_client):
    database = mongo_client[DB_NAME]

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
    return None


# Status------------------------------------------------------------------------


def count_trips_by_status(status: str, mongo_client):
    database = mongo_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": status}}
    stage_trip_count = {"$group": {"_id": None, "count": {"$sum": 1}}}
    pipeline = [stage_match_terminated_status, stage_trip_count]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["count"]
        # return 0 if len(data) == 0 else list(data)[0]["count"]
    return None


# Count------------------------------------------------------------------------


def count_trips(mongo_client):
    database = mongo_client[DB_NAME]

    stage_trip_count = {"$group": {"_id": None, "count": {"$sum": 1}}}
    pipeline = [stage_trip_count]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["count"]
    return None


def count_trips_new_count_today(mongo_client):
    database = mongo_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_match_today = {"$match": {"start": {"$gte": datetime.today()}}}
    stage_trip_count = {"$group": {"_id": None, "count": {"$sum": 1}}}
    pipeline = [stage_match_terminated_status, stage_match_today, stage_trip_count]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["count"]
    return None


def count_trips_new_countlast_n_days(amount: int, mongo_client):
    database = mongo_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}
    stage_match_last_n_days = {
        "$match": {"start": {"$gte": datetime.today() - timedelta(days=amount)}}
    }
    stage_trip_count = {"$group": {"_id": None, "count": {"$sum": 1}}}
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_days,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["count"]
    return None


def count_trips_new_countlast_n_days_range(amount: int, mongo_client):
    database = mongo_client[DB_NAME]

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
    return None


def count_trips_new_count_last_n_months(amount: int, mongo_client):
    database = mongo_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}

    stage_match_last_n_month = {
        "$match": {"start": {"$gte": datetime.today() - relativedelta(months=+amount)}}
    }
    stage_trip_count = {"$group": {"_id": None, "count": {"$sum": 1}}}
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_month,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["count"]
    return None


def count_trips_new_count_last_n_months_range(amount: int, mongo_client):
    database = mongo_client[DB_NAME]

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
    return None


def count_trips_new_count_last_n_years_range(amount: int, mongo_client):
    database = mongo_client[DB_NAME]

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
    return None


def count_trips_new_count_last_n_years_and_m_months_range(
    years: int, months: int, mongo_client
):
    database = mongo_client[DB_NAME]

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
    return None


def count_trips_new_count_last_n_years(amount: int, mongo_client):
    database = mongo_client[DB_NAME]

    stage_match_terminated_status = {"$match": {"status": "TERMINATED"}}

    stage_match_last_n_month = {
        "$match": {"start": {"$gte": datetime.today() - relativedelta(years=+amount)}}
    }
    stage_trip_count = {"$group": {"_id": None, "count": {"$sum": 1}}}
    pipeline = [
        stage_match_terminated_status,
        stage_match_last_n_month,
        stage_trip_count,
    ]

    data = database["trips"].aggregate(pipeline)
    if data is not None:
        return list(data)[0]["count"]
    return None

from fastapi import APIRouter, Request, HTTPException
from pymongo import MongoClient

from os import environ
import src.services.trips_metrics as services

MONGODB_URL = environ["MONGODB_URL"]
router = APIRouter()

# Duration----------------------------------------------------------------------


@router.get(
    "/duration/min", response_description="Get trip duration minimum in minutes"
)
def get_trip_duration_min(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.get_trip_duration_min(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/duration/max", response_description="Get trip duration maximum in minutes"
)
def get_trip_duration_max(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.get_trip_duration_max(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/duration/avg", response_description="Get trip duration average in minutes"
)
def get_trip_duration_avg(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.get_trip_duration_avg(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/duration/months/range", response_description="Count new trips last n months"
)
def count_trips_duration_last_n_months_range(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips_duration_last_n_months_range(amount, mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/duration/years-and-months/range",
    response_description="Count duratoin of trips last n months and years",
)
def count_trips_duration_last_n_years_and_m_months_range(
    years: int, months: int, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips_duration_last_n_years_and_m_months_range(
        years, months, mongo_client
    )
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/duration/years/range", response_description="Count new trips last n years"
)
def count_trips_duration_last_n_years_range(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips_duration_last_n_years_range(amount, mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/duration/days/range", response_description="Count new trips last n days")
def count_trips_duration_last_n_days_range(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips_duration_last_n_days_range(amount, mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


# Status------------------------------------------------------------------------


@router.get("/status/count", response_description="Count trips by status")
def count_trips_by_status(status: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips_by_status(status, mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


# Count------------------------------------------------------------------------


@router.get("/count", response_description="Count trips")
def count_trips(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/new/count/today", response_description="Count new trips by date")
def count_trips_new_count_today(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips_new_count_today(mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/new/count/days", response_description="Count new trips last n days")
def count_trips_new_countlast_n_days(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips_new_countlast_n_days(amount, mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/new/count/days/range", response_description="Count new trips last n days")
def count_trips_new_countlast_n_days_range(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips_new_countlast_n_days_range(amount, mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/new/count/months", response_description="Count new trips last n months")
def count_trips_new_count_last_n_months(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips_new_count_last_n_months(amount, mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/new/count/months/range", response_description="Count new trips last n months"
)
def count_trips_new_count_last_n_months_range(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips_new_count_last_n_months_range(amount, mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/new/count/years/range", response_description="Count new trips last n years"
)
def count_trips_new_count_last_n_years_range(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips_new_count_last_n_years_range(amount, mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get(
    "/new/count/years-and-months/range",
    response_description="Count new trips last n years",
)
def count_trips_new_count_last_n_years_and_m_months_range(
    years: int, months: int, request: Request
):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips_new_count_last_n_years_and_m_months_range(
        years, months, mongo_client
    )
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")


@router.get("/new/count/year", response_description="Count new trips last n years")
def count_trips_new_count_last_n_years(amount: int, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    data = services.count_trips_new_count_last_n_years(amount, mongo_client)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="Internal error")

@router.get(
    "/status/passenger/{id}/count", response_description="Count trips by status"
)
def count_trips_of_passenger_by_status(id: str, status: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    return services.count_trips_of_passenger_by_status(id, status, mongo_client)


@router.get("/status/driver/{id}/count", response_description="Count trips by status")
def count_trips_of_driver_by_status(id: str, status: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    return services.count_trips_of_driver_by_status(id, status, mongo_client)

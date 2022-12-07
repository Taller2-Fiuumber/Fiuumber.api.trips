from fastapi import APIRouter, Response, HTTPException, status

from src.domain.fare_calculator import lineal, calculate_test
from pymongo import MongoClient

from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

router = APIRouter()


@router.get("/fare", response_description="Get a calculated fare from coordinates")
def get_trip_fare(from_latitude, to_latitude, from_longitude, to_longitude):
    try:
        fare = lineal(
            float(from_latitude),
            float(to_latitude),
            float(from_longitude),
            float(to_longitude),
        )
        return Response(content=str(fare), media_type="application/json")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))


@router.get(
    "/fare/test", response_description="Get a calculated fare to test fare rule"
)
def get_trip_fare_to_test_fare_rule(
    fare_id: str = "3f000f2c-334d-4480-8ff2-d2cf5cdd235e",
    duration: float = 20,
    distance: float = 12,
    dailyTripAmountDriver: float = 15,
    dailyTripAmountPassenger: float = 2,
    monthlyTripAmountDrive: float = 100,
    monthlyTripAmountPassenger: float = 5,
    seniorityDriver: float = 2,
    seniorityPassenger: float = 1,
    recentTripAmount: float = 2,
):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]
        fare_rule = database["fare_rules"].find_one({"_id": fare_id})
        if (fare_rule) is not None:
            fare = calculate_test(
                fare_rule["minimum_fare"],
                fare_rule["duration_fare"],
                fare_rule["distance_fare"],
                fare_rule["dailyTripAmountDriver_fare"],
                fare_rule["dailyTripAmountPassenger_fare"],
                fare_rule["monthlyTripAmountDrive_fare"],
                fare_rule["monthlyTripAmountPassenger_fare"],
                fare_rule["seniorityDriver_fare"],
                fare_rule["seniorityPassenger_fare"],
                fare_rule["recentTripAmount_fare"],
                duration,
                distance,
                dailyTripAmountDriver,
                dailyTripAmountPassenger,
                monthlyTripAmountDrive,
                monthlyTripAmountPassenger,
                seniorityDriver,
                seniorityPassenger,
                recentTripAmount,
            )
        return Response(content=str(fare), media_type="application/json")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))

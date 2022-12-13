from fastapi import APIRouter, Response, HTTPException, status

import src.domain.fare_calculator as fare_calculator
from pymongo import MongoClient

from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

router = APIRouter()


@router.get("/fare", response_description="Get a calculated fare from coordinates")
def get_trip_fare(from_latitude, to_latitude, from_longitude, to_longitude):
    try:
        fare = fare_calculator.lineal(
            float(from_latitude),
            float(to_latitude),
            float(from_longitude),
            float(to_longitude),
        )
        return Response(content=str(fare), media_type="application/json")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))


@router.get(
    "/fare/final", response_description="Get a calculated fare from coordinates"
)
def get_trip_fare_final(
    passenger_id: str = 2,
    driver_id: str = 1,
    distance: float = 12,
    duration: float = 26,
):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]
        fare_rule = database["fare_rules"].find_one({"selected": True})

        if (fare_rule) is not None:
            fare = fare_calculator.calculate_final(
                fare_rule["minimum"],
                fare_rule["duration"],
                fare_rule["distance"],
                fare_rule["dailyTripAmountDriver"],
                fare_rule["dailyTripAmountPassenger"],
                fare_rule["monthlyTripAmountDrive"],
                fare_rule["monthlyTripAmountPassenger"],
                fare_rule["seniorityDriver"],
                fare_rule["seniorityPassenger"],
                fare_rule["recentTripAmount"],
                fare_rule["nightShift"],
                duration,
                distance,
                fare_calculator.daily_trip_amount_driver(driver_id),
                fare_calculator.daily_trip_amount_passenger(passenger_id),
                fare_calculator.monthly_trip_amount_driver(driver_id),
                fare_calculator.monthly_trip_amount_passenger(passenger_id),
                fare_calculator.get_driver_seniority(driver_id),
                fare_calculator.get_passenger_seniority(passenger_id),
                fare_calculator.get_recent_trip_amount(passenger_id),
                fare_calculator.is_night_shift(),
            )
            return Response(content=str(fare), media_type="application/json")
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There is no selected fare rule",
            )
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
    nightShift: float = 1,
):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        database = mongo_client.mongodb_client[DB_NAME]
        fare_rule = database["fare_rules"].find_one({"_id": fare_id})
        if (fare_rule) is not None:
            fare = fare_calculator.calculate_test(
                fare_rule["minimum"],
                fare_rule["duration"],
                fare_rule["distance"],
                fare_rule["dailyTripAmountDriver"],
                fare_rule["dailyTripAmountPassenger"],
                fare_rule["monthlyTripAmountDrive"],
                fare_rule["monthlyTripAmountPassenger"],
                fare_rule["seniorityDriver"],
                fare_rule["seniorityPassenger"],
                fare_rule["recentTripAmount"],
                fare_rule["nightShift"],
                duration,
                distance,
                dailyTripAmountDriver,
                dailyTripAmountPassenger,
                monthlyTripAmountDrive,
                monthlyTripAmountPassenger,
                seniorityDriver,
                seniorityPassenger,
                recentTripAmount,
                nightShift,
            )
        return Response(content=str(fare), media_type="application/json")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))


@router.get(
    "/fare/test/new", response_description="Get a calculated fare to test new fare rule"
)
def get_trip_fare_to_test_new_fare_rule(
    minimum_fare: float = 200,
    duration_fare: float = 0.1,
    distance_fare: float = 0.1,
    dailyTripAmountDriver_fare: float = 0.81,
    dailyTripAmountPassenger_fare: float = 0.1,
    monthlyTripAmountDrive_fare: float = 0.1,
    monthlyTripAmountPassenger_fare: float = 0.1,
    seniorityDriver_fare: float = -0.6,
    seniorityPassenger_fare: float = -0.3,
    recentTripAmount_fare: float = 0.2,
    nightShift_fare: float = 0.2,
    duration: float = 20,
    distance: float = 12,
    dailyTripAmountDriver: float = 15,
    dailyTripAmountPassenger: float = 2,
    monthlyTripAmountDrive: float = 100,
    monthlyTripAmountPassenger: float = 5,
    seniorityDriver: float = 2,
    seniorityPassenger: float = 1,
    recentTripAmount: float = 2,
    nightShift: float = 1,
):

    fare = fare_calculator.calculate_test(
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
        nightShift_fare,
        duration,
        distance,
        dailyTripAmountDriver,
        dailyTripAmountPassenger,
        monthlyTripAmountDrive,
        monthlyTripAmountPassenger,
        seniorityDriver,
        seniorityPassenger,
        recentTripAmount,
        nightShift,
    )
    return Response(content=str(fare), media_type="application/json")

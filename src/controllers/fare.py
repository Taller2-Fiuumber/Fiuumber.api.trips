from fastapi import APIRouter, Response, HTTPException, status

import src.services.fare as services
from pymongo import MongoClient

from os import environ

MONGODB_URL = environ["MONGODB_URL"]

router = APIRouter()


@router.get("/fare", response_description="Get a calculated fare from coordinates")
def get_trip_fare(from_latitude, to_latitude, from_longitude, to_longitude):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        fare = services.get_trip_fare(
            mongo_client, from_latitude, to_latitude, from_longitude, to_longitude
        )
        print(fare)
        return Response(content=str(fare), media_type="application/json")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))


@router.get(
    "/fare/final", response_description="Get a calculated fare from coordinates"
)
def get_trip_fare_final(
    passenger_id: str = "7897",
    driver_id: str = "9998",
    distance: float = 12,
    duration: float = 26,
):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        fare_rule = services.get_trip_fare_final(
            mongo_client, passenger_id, driver_id, distance, duration
        )

        if (fare_rule) is not None:
            return Response(content=str(fare_rule), media_type="application/json")
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
    monthlyTripAmountDriver: float = 100,
    monthlyTripAmountPassenger: float = 5,
    seniorityDriver: float = 2,
    seniorityPassenger: float = 1,
    recentTripAmount: float = 2,
):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        fare_rule = services.get_trip_fare_to_test_fare_rule(
            mongo_client,
            fare_id,
            duration,
            distance,
            dailyTripAmountDriver,
            dailyTripAmountPassenger,
            monthlyTripAmountDriver,
            monthlyTripAmountPassenger,
            seniorityDriver,
            seniorityPassenger,
            recentTripAmount,
        )
        if (fare_rule) is not None:
            return Response(content=str(fare_rule), media_type="application/json")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))


@router.get(
    "/fare/test/new", response_description="Get a calculated fare to test new fare rule"
)
def get_trip_fare_to_test_new_fare_rule(
    time_fare: float = 1,
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
    duration: float = 20,
    distance: float = 12,
    dailyTripAmountDriver: float = 15,
    dailyTripAmountPassenger: float = 2,
    monthlyTripAmountDriver: float = 100,
    monthlyTripAmountPassenger: float = 5,
    seniorityDriver: float = 2,
    seniorityPassenger: float = 1,
    recentTripAmount: float = 2,
):
    try:
        fare = services.get_trip_fare_to_test_new_fare_rule(
            time_fare,
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
            monthlyTripAmountDriver,
            monthlyTripAmountPassenger,
            seniorityDriver,
            seniorityPassenger,
            recentTripAmount,
        )
        if fare:
            return Response(content=str(fare), media_type="application/json")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))

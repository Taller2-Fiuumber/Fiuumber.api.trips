from fastapi import APIRouter, Body, HTTPException

import src.services.payments as services
from src.domain.payment import Payment
from src.utils.payments_processor import process_payments, create_trip_payments

from src.domain.trip_id import TripId

from pymongo import MongoClient

from os import environ

MONGODB_URL = environ["MONGODB_URL"]

router = APIRouter()


@router.get(
    "/process",
    response_description="Process all pending payments for trips",
)
def process():
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    try:
        return process_payments(mongo_client)
    except Exception as ex:
        detail = f"Cannot process payments: {str(ex)}"
        raise HTTPException(status_code=500, detail=detail)


@router.post(
    "/create-for-trip",
    response_description="Generate payments from processed trip",
)
def create_for_trip(params: TripId = Body(...)):
    try:
        return create_trip_payments(params.trip_id)
    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Cannot create payments for trip: {str(ex)}"
        )


# TODO: eliminar este endpoint, no debería exponerse
@router.post(
    "",
    response_description="Creates a new payment",
)
def create(payment: Payment = Body(...)):
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)

        return services.create_payment(payment, mongo_client)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Cannot create payment: {str(ex)}")


@router.get(
    "",
    response_description="Get all payments",
)
def get():
    try:
        mongo_client = MongoClient(MONGODB_URL, connect=False)
        return services.get_all_payments(mongo_client)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Cannot get payments: {str(ex)}")

from fastapi import APIRouter, Request, Response, Body, HTTPException
from pymongo import MongoClient

import src.dal.payments_provider as payments_provider
from src.domain.payment import Payment

router = APIRouter()

@router.get(
    "/process",
    response_description="Process all pending payments for trips",
)
def process(request: Request):
    try:
        pending_payments = payments_provider.get_pending_payments()
        for payment in pending_payments:
            print(payment)
        return pending_payments
    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Cannot process payments" + str(ex)
        )

# TODO: eliminar este endpoint, no debería exponerse
@router.post(
    "/",
    response_description="Creates a new payment",
)
def create(payment: Payment = Body(...)):
    try:
        return payments_provider.create_payment(payment)
    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Cannot create payment: " + str(ex)
        )


@router.get(
    "/",
    response_description="Get all payments",
)
def get():
    try:
        payments = payments_provider.get_all_payments()
        print(payments)
        return payments
    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Cannot get payments" + str(ex)
        )
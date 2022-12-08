from fastapi import APIRouter, Body, HTTPException

import src.dal.payments_provider as payments_provider
from src.domain.payment import Payment
from src.utils.payments_processor import process_payment, create_trip_payments

from pydantic import BaseModel, Field


class TripId(BaseModel):
    trip_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "trip_id": "15576e35-390a-478b-bd05-0572c023bdee",
            }
        }
        orm_mode = True


router = APIRouter()


@router.get(
    "/process",
    response_description="Process all pending payments for trips",
)
def process():
    try:
        pending_payments = payments_provider.get_pending_payments()
        for payment in pending_payments:
            try:
                print("[INFO] processing payment: " + payment["_id"])
                payments_provider.mark_payment_as_processing(payment["_id"])
                hash = process_payment(payment)
                payments_provider.mark_payment_as_processed(payment["_id"], hash)
            except Exception:
                continue
        return pending_payments
    except Exception as ex:
        detail = f"Cannot process payments: {str(ex)}"
        raise HTTPException(status_code=500, detail=detail)


@router.post(
    "/create-for-trip",
    response_description="Generate payments from proccessed trip",
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
        return payments_provider.create_payment(payment)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Cannot create payment: {str(ex)}")


@router.get(
    "",
    response_description="Get all payments",
)
def get():
    try:
        return payments_provider.get_all_payments()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Cannot get payments: {str(ex)}")

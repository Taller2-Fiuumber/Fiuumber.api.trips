from fastapi import APIRouter, Body, HTTPException

import src.dal.payments_provider as payments_provider
from src.domain.payment import Payment
from src.utils.payments_processor import process_payment, create_trip_payments

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


# @router.get(
#     "/generate",
#     response_description="Generate payments from proccessed",
# )
# def process():
#     try:
#         incomplete_payments = payments_provider.get_incomplete_payments()
#         for payment in incomplete_payments:
#             try:

#             except Exception as ex:
#                 continue
#         return incomplete_payments
#     except Exception as ex:
#         raise HTTPException(
#             status_code=500, detail=f"Cannot process payments" + str(ex)
#         )


@router.get(
    "/create-for-trip",
    response_description="Generate payments from proccessed",
)
def create_for_trip():
    try:
        return create_trip_payments("15576e35-390a-478b-bd05-0572c023bdee")
    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Cannot process payments: {str(ex)}"
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
        payments = payments_provider.get_all_payments()
        return payments
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Cannot get payments{ str(ex)}")

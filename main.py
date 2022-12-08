# docuemntation: https://www.mongodb.com/languages/python/pymongo-tutorial

from fastapi import FastAPI

from src.services.trips import router as trip_router
from src.services.trips_metrics import router as trips_metrics_router

from src.services.trips_status import router as trips_status_router

from src.services.fare import router as fare_router
from src.services.fare_rules import router as fare_rules_router
from src.services.fare_metrics import router as fare_metrics_router

from src.services.calification import router as calification_router
from src.services.calification_metrics import router as calification_metrics_router

from src.services.payments import router as payments_router


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Fiuumber API Trips"}


app.include_router(trip_router, tags=["trips"], prefix="/api/trips")
app.include_router(
    trips_metrics_router, tags=["trips metrics"], prefix="/api/trips/metrics/trips"
)

app.include_router(trips_status_router, tags=["status"], prefix="/api/trips")

app.include_router(fare_router, tags=["fare"], prefix="/api/trips")
app.include_router(fare_rules_router, tags=["fare rules"], prefix="/api/trips")
app.include_router(
    fare_metrics_router, tags=["fare metrics"], prefix="/api/trips/metrics/fares"
)

app.include_router(calification_router, tags=["calification"], prefix="/api/trips")
app.include_router(
    calification_metrics_router,
    tags=["calification metrics"],
    prefix="/api/trips/metrics/calification",
)

app.include_router(payments_router, tags=["payments"], prefix="/api/trips/payments")

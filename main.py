# docuemntation: https://www.mongodb.com/languages/python/pymongo-tutorial

from fastapi import FastAPI
from src.services.routes import router as trip_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Fiuumber API Trips"}


app.include_router(trip_router, tags=["trips"], prefix="/api/trips")

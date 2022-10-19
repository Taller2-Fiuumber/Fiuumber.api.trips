from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from src.domain.trip import Trip, TripUpdate

router = APIRouter()


@router.post(
    "/trip",
    response_description="Create a new trip",
    status_code=status.HTTP_201_CREATED,
    response_model=Trip,
)
def create_trip(request: Request, trip: Trip = Body(...)):
    trip = jsonable_encoder(trip)
    new_trip = request.app.database["trips"].insert_one(trip)
    created_trip = request.app.database["trips"].find_one({"_id": new_trip.inserted_id})

    return created_trip


@router.get("/trips", response_description="List all trips", response_model=List[Trip])
def list_trips(request: Request):
    trips = list(request.app.database["trips"].find(limit=100))
    return trips


@router.get(
    "/trip/id={id}", response_description="Get a single trip by id", response_model=Trip
)
def find_trip(id: str, request: Request):
    if (trip := request.app.database["trips"].find_one({"_id": id})) is not None:
        return trip
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.put("/trip/id={id}", response_description="Update a trip", response_model=Trip)
def update_trip(id: str, request: Request, trip: TripUpdate = Body(...)):
    trip = {k: v for k, v in trip.dict().items() if v is not None}
    if len(trip) >= 1:
        update_result = request.app.database["trips"].update_one(
            {"_id": id}, {"$set": trip}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trip with ID {id} not found",
            )

    if (
        existing_trip := request.app.database["trips"].find_one({"_id": id})
    ) is not None:
        return existing_trip

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )


@router.delete("/trip/id={id}", response_description="Delete a trip")
def delete_trip(id: str, request: Request, response: Response):
    delete_result = request.app.database["trips"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with ID {id} not found"
    )

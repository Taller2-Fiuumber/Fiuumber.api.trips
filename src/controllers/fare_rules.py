from fastapi import APIRouter, HTTPException, status, Body, Request
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from src.domain.fare_rule import FareRule
import src.services.fare_rules as services

from os import environ

MONGODB_URL = environ["MONGODB_URL"]

router = APIRouter()


@router.get("/fare-rule/selected", response_description="Get selected fare")
def get_selected_fare(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    selected_rule = services.get_selected_fare(mongo_client)

    if selected_rule is not None:
        return selected_rule
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No fare rule is selected",
    )


@router.post(
    "/fare-rule",
    response_description="Create a fare rule",
    status_code=status.HTTP_201_CREATED,
)
def create_fare_rule(request: Request, fare_rule: FareRule = Body(...)):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    new_fare_rule = services.create_fare_rule(mongo_client, jsonable_encoder(fare_rule))

    if new_fare_rule is not None:
        return new_fare_rule
    raise HTTPException(
        status_code=401, detail="Fare rule with ID not created successfully"
    )


@router.get("/fare-rules", response_description="List all fare rules")
def list_fare_rules(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    fare_rules = services.list_fare_rules(mongo_client)
    if fare_rules is not None:
        return list(fare_rules)
    return None


@router.get("/fare-rule/{id}", response_description="Get a single fare rule by id")
def find_fare_rules_by_id(id: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    fare_rule = services.find_fare_rules_by_id(id, mongo_client)
    if fare_rule is not None:
        return fare_rule
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Fare rule with ID {id} not found",
    )


@router.post("/fare-rule/select/{id}", response_description="Select a fare rule")
def select_a_fare_rule(id: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)

    new_selected_fare_rule = services.select_a_fare_rule(id, mongo_client)

    if new_selected_fare_rule is not None:
        return new_selected_fare_rule
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Fare rule with ID {id} not found",
    )

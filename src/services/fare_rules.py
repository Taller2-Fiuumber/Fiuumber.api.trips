from fastapi import APIRouter, HTTPException, status, Body, Request
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from src.domain.fare_rule import FareRule

from os import environ

MONGODB_URL = environ["MONGODB_URL"]
DB_NAME = environ["DB_NAME"]

router = APIRouter()


@router.get("/fare-rule/selected", response_description="Get selected fare")
def get_selected_fare(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    selected_rule = database["fare_rules"].find_one({"selected": True})

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
def create_fare_rule(request: Request, rule: FareRule = Body(...)):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    fare_rule = jsonable_encoder(rule)
    new_fare_rule = database["fare_rules"].insert_one(fare_rule)
    created_new_fare_rule = database["fare_rules"].find_one(
        {"_id": new_fare_rule.inserted_id}
    )

    if created_new_fare_rule is not None:
        return created_new_fare_rule
    raise HTTPException(
        status_code=401, detail="Fare rule with ID not created successfully"
    )


@router.get("/fare-rules", response_description="List all fare rules")
def list_fare_rules(request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    fare_rules = database["fare_rules"].find()
    return list(fare_rules)


@router.get("/fare-rule/{id}", response_description="Get a single fare rule by id")
def find_fare_rules_by_id(id: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    if (fare_rule := database["fare_rules"].find_one({"_id": id})) is not None:
        return fare_rule
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Fare rule with ID {id} not found",
    )


@router.post("/fare-rule/select/{id}", response_description="Select a fare rule")
def select_a_fare_rule(id: str, request: Request):
    mongo_client = MongoClient(MONGODB_URL, connect=False)
    database = mongo_client.mongodb_client[DB_NAME]

    old_selected_fare_rule = database["fare_rules"].find_one({"selected": True})
    new_selected_fare_rule = database["fare_rules"].update_one(
        {"_id": id}, {"$set": {"selected": True}}
    )

    if new_selected_fare_rule is not None:
        if old_selected_fare_rule is not None:
            database["fare_rules"].update_one(
                {"_id": old_selected_fare_rule["_id"]}, {"$set": {"selected": False}}
            )
        return database["fare_rules"].find_one({"_id": id})
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Fare rule with ID {id} not found",
    )

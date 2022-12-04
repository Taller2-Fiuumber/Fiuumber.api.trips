import uuid
from pydantic import BaseModel, Field
import datetime


class FareRule(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    selected: bool = False,
    createdAt: datetime.datetime = Field(...)
    updatedAt: datetime.datetime = Field(...)
    minimum_fare: float = 0,
    duration_fare: float = 0,
    distance_fare: float = 0,
    dailyTripAmountDriver_fare: float = 0,
    dailyTripAmountPassenger_fare: float = 0,
    monthlyTripAmountDrive_fare: float = 0,
    monthlyTripAmountPassenger_fare: float = 0,
    seniorityDriver_fare: float = 0,
    seniorityPassenger_fare: float = 0,
    recentTripAmount_fare: float = 0,

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "selected": False,
                "createdAt": datetime.datetime(2022, 9, 9, 2),
                "updatedAt": datetime.datetime(2022, 9, 9, 2),
                "minimum_fare": 200.0,
                "duration_fare": 5,
                "distance_fare": 6,
                "dailyTripAmountDriver_fare": 0.7,
                "dailyTripAmountPassenger_fare": -0.7,
                "monthlyTripAmountDrive_fare": 0.8,
                "monthlyTripAmountPassenger_fare": -0.8,
                "seniorityDriver_fare": 0.5,
                "seniorityPassenger_fare": -0.25,
                "recentTripAmount_fare": -0.2,
            }
        }
        orm_mode = True


class FareRuleUpdate(BaseModel):
    minimum_fare: float = 0
    duration: float = Field(...)
    createdAt: datetime.datetime = Field(...)
    distance: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "selected": True,
                "createdAt": datetime.datetime(2022, 9, 9, 2),
                "updatedAt": datetime.datetime(2022, 11, 10, 2),
                "minimum_fare": 200.0,
                "duration_fare": 5,
                "distance_fare": 6,
                "dailyTripAmountDriver_fare": 0.7,
                "dailyTripAmountPassenger_fare": -0.7,
                "monthlyTripAmountDrive_fare": 0.8,
                "monthlyTripAmountPassenger_fare": -0.8,
                "seniorityDriver_fare": 0.5,
                "seniorityPassenger_fare": -0.25,
                "recentTripAmount_fare": -0.2,
                "createdAt": datetime.datetime(2022, 9, 9, 2),
                "minimum_fare": 400,
                "price_per_minute": 0.3,
                "price_per_km": 0.5,
            }
        }
        orm_mode = True

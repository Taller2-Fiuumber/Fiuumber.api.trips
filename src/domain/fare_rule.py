import uuid
from pydantic import BaseModel, Field
import datetime


class FareRule(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    selected: bool = (False,)
    createdAt: datetime.datetime = (datetime.datetime.now(),)
    updatedAt: datetime.datetime = (datetime.datetime.now(),)
    minimum: float = (0,)
    duration: float = (0,)
    distance: float = (0,)
    dailyTripAmountDriver: float = (0,)
    dailyTripAmountPassenger: float = (0,)
    monthlyTripAmountDriver: float = (0,)
    monthlyTripAmountPassenger: float = (0,)
    seniorityDriver: float = (0,)
    seniorityPassenger: float = (0,)
    recentTripAmount: float = (0,)
    nightShift: float = (0,)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "selected": False,
                "minimum": 200.0,
                "duration": 5,
                "distance": 6,
                "dailyTripAmountDriver": 0.7,
                "dailyTripAmountPassenger": -0.7,
                "monthlyTripAmountDriver": 0.8,
                "monthlyTripAmountPassenger": -0.8,
                "seniorityDriver": 0.5,
                "seniorityPassenger": -0.25,
                "recentTripAmount": -0.2,
                "nightShift": 0.1,
            }
        }
        orm_mode = True


class FareRuleUpdate(BaseModel):
    minimum: float = 0
    duration: float = Field(...)
    createdAt: datetime.datetime = Field(...)
    distance: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "selected": True,
                "minimum": 200.0,
                "duration": 5,
                "distance": 6,
                "dailyTripAmountDriver": 0.7,
                "dailyTripAmountPassenger": -0.7,
                "monthlyTripAmountDriver": 0.8,
                "monthlyTripAmountPassenger": -0.8,
                "seniorityDriver": 0.5,
                "seniorityPassenger": -0.25,
                "recentTripAmount": -0.2,
                "price_per_minute": 0.3,
                "price_per_km": 0.5,
                "nightShift": 0.1,
            }
        }
        orm_mode = True

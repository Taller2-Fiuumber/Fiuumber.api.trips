import uuid
from pydantic import BaseModel, Field
import datetime


class FareRule(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    minimum_fare: float = 0
    duration: float = Field(...)
    createdAt: datetime.datetime = Field(...)
    distance: float = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "createdAt": datetime.datetime(2022, 9, 9, 2),
                "minimum_fare": 400,
                "price_per_minute": 0.3,
                "price_per_km": 0.5,
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
                "createdAt": datetime.datetime(2022, 9, 9, 2),
                "minimum_fare": 400,
                "price_per_minute": 0.3,
                "price_per_km": 0.5,
            }
        }
        orm_mode = True

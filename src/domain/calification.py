import uuid
from pydantic import BaseModel, Field
import datetime


class Calification(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    passengerId: str = Field(...)
    driverId: str = Field(...)
    tripId: str = Field(...)
    createdAt: datetime.datetime = Field(...)
    updatedAt: datetime.datetime = Field(...)
    stars: int = Field(...)
    comments: str = Field(...)
    reviewer: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "passengerId": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "driverId": "2320930329-b04a-4b30-b46c-fsdfwefwefw",
                "tripId": "ddfdsfsdf-b04a-4b30-b4sdf6c-fsdtjkjj",
                "createdAt": datetime.datetime.now(),
                "updatedAt": datetime.datetime.now(),
                "stars": 5,
                "comments": "Nice driver. Love the scene.",
                "reviewer": "PASSENGER",
            }
        }
        orm_mode = True


class CalificationUpdate(BaseModel):
    passengerId: str = Field(...)
    driverId: str = Field(...)
    tripId: str = Field(...)
    createdAt: datetime.datetime = Field(...)
    updatedAt: datetime.datetime = Field(...)
    stars: int = Field(...)
    comments: str = Field(...)
    reviewer: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "passengerId": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "driverId": "2320930329-b04a-4b30-b46c-fsdfwefwefw",
                "tripId": "ddfdsfsdf-b04a-4b30-b4sdf6c-fsdtjkjj",
                "createdAt": datetime.datetime(2022, 7, 4),
                "updatedAt": datetime.datetime.now(),
                "stars": 5,
                "comments": "Nice driver. Love the scene.",
                "reviewer": "PASSENGER",
            }
        }
        orm_mode = True

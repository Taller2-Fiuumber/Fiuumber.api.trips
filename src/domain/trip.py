import uuid
from pydantic import BaseModel, Field
import datetime


class Trip(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    passengerId: str = Field(...)
    driverId: str = Field(...)
    from_latitude: float = Field(...)
    from_longitude: float = Field(...)
    to_latitude: float = Field(...)
    to_longitude: float = Field(...)
    start: datetime.datetime = Field(...)
    finish: datetime.datetime = Field(...)
    subscription: str = Field(...)
    status: str = Field(...)
    finalPrice: float = Field(...)
    from_address: str = Field(...)
    to_address: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "passengerId": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "driverId": "2320930329-b04a-4b30-b46c-fsdfwefwefw",
                "from_latitude": -34.603683,
                "from_longitude": -58.381557,
                "to_latitude": -34.6175841,
                "to_longitude": -58.3682286,
                "start": datetime.datetime(2022, 9, 9, 2),
                "finish": datetime.datetime(2022, 9, 10, 5),
                "subscription": "VIP",
                "status": "Done",
                "finalPrice": 532.50,
                "from_address": "Calle Falsa 123",
                "to_address": "Calle Falsa 666",
            }
        }
        orm_mode = True


class TripUpdate(BaseModel):
    passengerId: str = Field(...)
    driverId: str = Field(...)
    from_latitude: float = Field(...)
    from_longitude: float = Field(...)
    to_latitude: float = Field(...)
    to_longitude: float = Field(...)
    start: datetime.datetime = Field(...)
    finish: datetime.datetime = Field(...)
    subscription: str = Field(...)
    status: str = Field(...)
    finalPrice: float = Field(...)
    from_address: str = Field(...)
    to_address: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "passengerId": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "driverId": "2320930329-b04a-4b30-b46c-fsdfwefwefw",
                "from_latitude": -34.603683,
                "from_longitude": -58.381557,
                "to_latitude": -34.6175841,
                "to_longitude": -58.3682286,
                "to_location": "Don Quixote",
                "start": datetime.datetime(2022, 9, 9, 0),
                "finish": datetime.datetime(2022, 9, 10, 5),
                "subscription": "VIP",
                "status": "Done",
                "finalPrice": 532.50,
                "from_address": "Calle Falsa 123",
                "to_address": "Calle Falsa 666",
            }
        }
        orm_mode = True

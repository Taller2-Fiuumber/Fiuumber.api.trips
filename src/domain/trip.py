import uuid
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Trip(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    passengerId: str = Field(...)
    driverId: str = Field(...)
    from_latitude: float = Field(...)
    from_longitude: float = Field(...)
    to_latitude: float = Field(...)
    to_longitude: float = Field(...)
    start: Optional[datetime] = None
    finish: Optional[datetime] = None
    subscription: str = Field(...)
    status: str = Field(...)
    finalPrice: float = Field(...)
    from_address: str = Field(...)
    to_address: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "passengerId": "12",
                "driverId": "27",
                "from_latitude": -34.603683,
                "from_longitude": -58.381557,
                "to_latitude": -34.6175841,
                "to_longitude": -58.3682286,
                "subscription": "REGULAR",
                "status": "REQUESTED",
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
    start: Optional[datetime] = None
    finish: Optional[datetime] = None
    subscription: str = Field(...)
    status: str = Field(...)
    finalPrice: float = Field(...)
    from_address: str = Field(...)
    to_address: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "passengerId": "12",
                "driverId": "27",
                "from_latitude": -34.603683,
                "from_longitude": -58.381557,
                "to_latitude": -34.6175841,
                "to_longitude": -58.3682286,
                "to_location": "Don Quixote",
                "subscription": "VIP",
                "status": "Done",
                "finalPrice": 532.50,
                "from_address": "Calle Falsa 123",
                "to_address": "Calle Falsa 666",
            }
        }
        orm_mode = True

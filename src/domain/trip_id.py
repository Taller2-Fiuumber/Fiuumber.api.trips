from pydantic import BaseModel, Field


class TripId(BaseModel):
    trip_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "trip_id": "15576e35-390a-478b-bd05-0572c023bdee",
            }
        }
        orm_mode = True

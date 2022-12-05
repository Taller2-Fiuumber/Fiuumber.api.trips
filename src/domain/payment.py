import uuid
from pydantic import BaseModel, Field
import datetime
from typing import Optional

class Payment(BaseModel):

    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    tripId: Optional[str] = Field(...)
    createdAt: datetime.datetime = datetime.datetime.now()
    updatedAt: datetime.datetime = datetime.datetime.now()
    processedAt: datetime.datetime = None
    startedProcessing: datetime.datetime = None
    ammount: float = Field(...)
    tx_hash: str = None
    wallet_address: str = Field(...) # Segun el campo type, puede ser la de origen o la de destino
    type: str = Field(...)
    order: Optional[int] = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "tripId": "ddfdsfsdf-b04a-4b30-b4sdf6c-fsdtjkjj",
                "createdAt": datetime.datetime.now(),
                "updatedAt": datetime.datetime.now(),
                "processedAt": datetime.datetime.now(),
                "ammount": 0.00000001,
                "tx_hash": "0x030d20dab0b53c123a12f2696a5c8bd23f449789d677a1571e1cdea6eacf0285",
                "type": "FROM_SENDER",
                "wallet_address": "",
                "order": 1,
            }
        }
        orm_mode = True


class PaymentUpdate(BaseModel):
    tripId: str = Field(...)
    createdAt: datetime.datetime = datetime.datetime.now()
    updatedAt: datetime.datetime = datetime.datetime.now()
    processedAt: datetime.datetime = None
    ammount: float = Field(...)
    tx_hash: str = None
    type: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "tripId": "ddfdsfsdf-b04a-4b30-b4sdf6c-fsdtjkjj",
                "createdAt": datetime.datetime.now(),
                "updatedAt": datetime.datetime.now(),
                "processedAt": datetime.datetime.now(),
                "ammount": 0.00000001,
                "tx_hash": "0x030d20dab0b53c123a12f2696a5c8bd23f449789d677a1571e1cdea6eacf0285",
                "type": "TO_RECEIVER",
                "wallet_address": "",
            }
        }
        orm_mode = True

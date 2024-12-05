from pydantic import BaseModel
from typing import Optional, List


class Good(BaseModel):
    name: str
    price: float


class GoodDetails(BaseModel):
    name: str
    price: float
    description: Optional[str] = ""
    count: int


class SaleRequest(BaseModel):
    username: str
    good_name: str


class SaleResponse(BaseModel):
    message: str
    remaining_balance: float
    purchased_item: str


class AddGoodRequest(BaseModel):
    name: str
    price: float
    count: int
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Smartphone",
                "price": 699.99,
                "count": 50,
                "description": "A high-end smartphone with 128GB storage"
            }
        }

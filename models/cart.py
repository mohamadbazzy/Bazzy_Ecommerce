from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId
from app.models.pyobjectid import PyObjectId

class CartItem(BaseModel):
    product_id: PyObjectId
    quantity: int

class CartModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    items: List[CartItem]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

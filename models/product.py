from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from app.models.pyobjectid import PyObjectId


class ProductModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str]
    price: float
    category_id: PyObjectId
    stock: int

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

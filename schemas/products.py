# app/schemas/product.py

from pydantic import BaseModel, Field, PositiveInt, PositiveFloat
from typing import Optional, List
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: PositiveFloat
    quantity: PositiveInt
    category: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = Field(default_factory=list)
    # Add more fields as necessary

    class Config:
        schema_extra = {
            "example": {
                "name": "Wireless Mouse",
                "description": "A high-precision wireless mouse.",
                "price": 29.99,
                "quantity": 150,
                "category": "Electronics",
                "tags": ["accessories", "computer", "wireless"]
            }
        }

class ProductCreate(ProductBase):
    pass  # Inherits all fields from ProductBase

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[PositiveFloat] = None
    quantity: Optional[PositiveInt] = None
    category: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = None
    # Add more fields as necessary

    class Config:
        schema_extra = {
            "example": {
                "price": 24.99,
                "quantity": 200,
                "tags": ["updated", "sale"]
            }
        }

class ProductOut(ProductBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

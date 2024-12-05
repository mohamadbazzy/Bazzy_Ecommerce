"""
Product Models Module.

This module defines the `ProductModel` class, representing products within the application.
It utilizes Pydantic for data validation and integrates with MongoDB through the custom `PyObjectId`.
"""

from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from app.models.pyobjectid import PyObjectId


class ProductModel(BaseModel):
    """
    Product Model.

    Represents a product available within the application.

    Attributes:
        id (PyObjectId): The unique identifier for the product, mapped from MongoDB's `_id`.
        name (str): The name of the product.
        description (Optional[str]): A brief description of the product.
        price (float): The price of the product.
        category_id (PyObjectId): The identifier of the category this product belongs to.
        stock (int): The available stock quantity for the product.
    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str]
    price: float
    category_id: PyObjectId
    stock: int

    class Config:
        """
        Configuration for the `ProductModel`.

        Allows arbitrary types and defines JSON encoders for `ObjectId`.
        """

        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

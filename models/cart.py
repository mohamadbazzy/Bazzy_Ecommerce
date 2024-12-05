"""
Cart Models Module.

This module defines the data models related to shopping carts, including `CartItem` and `CartModel`.
It utilizes Pydantic for data validation and MongoDB's `ObjectId` for unique identifiers.
"""

from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId
from app.models.pyobjectid import PyObjectId


class CartItem(BaseModel):
    """
    Cart Item Model.

    Represents an individual item within a shopping cart.

    Attributes:
        product_id (PyObjectId): The unique identifier of the product.
        quantity (int): The quantity of the product in the cart.
    """

    product_id: PyObjectId
    quantity: int


class CartModel(BaseModel):
    """
    Shopping Cart Model.

    Represents a user's shopping cart containing multiple items.

    Attributes:
        id (PyObjectId): The unique identifier for the cart, mapped from MongoDB's `_id`.
        user_id (PyObjectId): The identifier of the user owning the cart.
        items (List[CartItem]): A list of items in the cart.
    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    items: List[CartItem]

    class Config:
        """
        Configuration for the `CartModel`.

        Allows arbitrary types and defines JSON encoders for `ObjectId`.
        """
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

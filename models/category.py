"""
Category Models Module.

This module defines the `CategoryModel` class, representing product categories within the application.
It utilizes Pydantic for data validation and integrates with MongoDB through the custom `PyObjectId`.
"""

from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from app.models.pyobjectid import PyObjectId


class CategoryModel(BaseModel):
    """
    Category Model.

    Represents a product category within the application.

    Attributes:
        id (PyObjectId): The unique identifier for the category, mapped from MongoDB's `_id`.
        name (str): The name of the category.
        description (Optional[str]): A brief description of the category.
    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str]

    class Config:
        """
        Configuration for the `CategoryModel`.

        Allows arbitrary types and defines JSON encoders for `ObjectId`.
        """

        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

"""
Products Schemas Module.

This module defines the Pydantic models related to product operations, including
product creation, updating, and output representations. These schemas are used for
validating and serializing data in product-related API endpoints.
"""

from pydantic import BaseModel, Field, PositiveInt, PositiveFloat
from typing import Optional, List
from bson import ObjectId


class PyObjectId(ObjectId):
    """
    Custom PyObjectId Type.

    Extends MongoDB's `ObjectId` to integrate seamlessly with Pydantic models,
    enabling validation and serialization of ObjectId fields.
    """

    @classmethod
    def __get_validators__(cls):
        """
        Yield validator functions for Pydantic.

        Yields:
            Callable: The validator method for `PyObjectId`.
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """
        Validate and convert input to an `ObjectId`.

        Args:
            v (str | ObjectId): The value to validate and convert.

        Returns:
            ObjectId: The validated `ObjectId`.

        Raises:
            ValueError: If the input is not a valid `ObjectId`.
        """
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class ProductBase(BaseModel):
    """
    Base Product Schema.

    Defines the common structure for product-related operations.

    Attributes:
        name (str): The name of the product.
        description (Optional[str]): A brief description of the product.
        price (PositiveFloat): The price of the product.
        quantity (PositiveInt): The available quantity of the product.
        category (Optional[str]): The category of the product.
        tags (Optional[List[str]]): A list of tags associated with the product.
    """

    name: str = Field(
        ..., min_length=1, max_length=100, description="The name of the product."
    )
    description: Optional[str] = Field(
        None, max_length=500, description="A brief description of the product."
    )
    price: PositiveFloat = Field(
        ..., description="The price of the product."
    )
    quantity: PositiveInt = Field(
        ..., description="The available quantity of the product."
    )
    category: Optional[str] = Field(
        None, max_length=50, description="The category of the product."
    )
    tags: Optional[List[str]] = Field(
        default_factory=list, description="A list of tags associated with the product."
    )
    # Add more fields as necessary

    class Config:
        """
        Configuration for the ProductBase Schema.

        Provides example data for documentation purposes.
        """

        schema_extra = {
            "example": {
                "name": "Wireless Mouse",
                "description": "A high-precision wireless mouse.",
                "price": 29.99,
                "quantity": 150,
                "category": "Electronics",
                "tags": ["accessories", "computer", "wireless"],
            }
        }


class ProductCreate(ProductBase):
    """
    Product Creation Schema.

    Inherits from `ProductBase` and is used for creating new products.
    """
    pass  # Inherits all fields from ProductBase


class ProductUpdate(BaseModel):
    """
    Product Update Schema.

    Defines the structure for updating an existing product.

    Attributes:
        name (Optional[str]): The new name of the product.
        description (Optional[str]): The new description of the product.
        price (Optional[PositiveFloat]): The new price of the product.
        quantity (Optional[PositiveInt]): The new available quantity of the product.
        category (Optional[str]): The new category of the product.
        tags (Optional[List[str]]): The new list of tags associated with the product.
    """

    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="The new name of the product."
    )
    description: Optional[str] = Field(
        None, max_length=500, description="The new description of the product."
    )
    price: Optional[PositiveFloat] = Field(
        None, description="The new price of the product."
    )
    quantity: Optional[PositiveInt] = Field(
        None, description="The new available quantity of the product."
    )
    category: Optional[str] = Field(
        None, max_length=50, description="The new category of the product."
    )
    tags: Optional[List[str]] = Field(
        None, description="The new list of tags associated with the product."
    )
    # Add more fields as necessary

    class Config:
        """
        Configuration for the ProductUpdate Schema.

        Provides example data for documentation purposes.
        """

        schema_extra = {
            "example": {
                "price": 24.99,
                "quantity": 200,
                "tags": ["updated", "sale"],
            }
        }


class ProductOut(ProductBase):
    """
    Product Output Schema.

    Defines the structure for the product information returned by the API.

    Attributes:
        id (PyObjectId): The unique identifier of the product.
    """

    id: PyObjectId = Field(
        default_factory=PyObjectId, alias="_id", description="The unique identifier of the product."
    )

    class Config:
        """
        Configuration for the ProductOut Schema.

        Enables ORM mode and defines JSON encoders for ObjectId.
        """

        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

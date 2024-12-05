"""
Sales Schemas Module.

This module defines the Pydantic models related to sales operations, including
displaying goods, processing sales transactions, and adding new goods. These schemas are used for
validating and serializing data in sales-related API endpoints.
"""

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt
from typing import Optional, List


class Good(BaseModel):
    """
    Good Schema.

    Defines the structure for basic good information.

    Attributes:
        name (str): The name of the good.
        price (float): The price of the good.
    """

    name: str = Field(
        ..., description="The name of the good."
    )
    price: float = Field(
        ..., description="The price of the good."
    )


class GoodDetails(BaseModel):
    """
    Good Details Schema.

    Defines the structure for detailed good information.

    Attributes:
        name (str): The name of the good.
        price (float): The price of the good.
        description (Optional[str]): A brief description of the good.
        count (int): The available quantity of the good.
    """

    name: str = Field(
        ..., description="The name of the good."
    )
    price: float = Field(
        ..., description="The price of the good."
    )
    description: Optional[str] = Field(
        "", description="A brief description of the good."
    )
    count: int = Field(
        ..., description="The available quantity of the good."
    )


class SaleRequest(BaseModel):
    """
    Sale Request Schema.

    Defines the structure for processing a sale transaction.

    Attributes:
        username (str): The username of the customer making the purchase.
        good_name (str): The name of the good being purchased.
    """

    username: str = Field(
        ..., description="The username of the customer making the purchase."
    )
    good_name: str = Field(
        ..., description="The name of the good being purchased."
    )


class SaleResponse(BaseModel):
    """
    Sale Response Schema.

    Defines the structure for the response after processing a sale transaction.

    Attributes:
        message (str): A confirmation message indicating the sale was processed.
        remaining_balance (float): The remaining balance in the user's wallet after the sale.
        purchased_item (str): The name of the item that was purchased.
    """

    message: str = Field(
        ..., description="A confirmation message indicating the sale was processed."
    )
    remaining_balance: float = Field(
        ..., description="The remaining balance in the user's wallet after the sale."
    )
    purchased_item: str = Field(
        ..., description="The name of the item that was purchased."
    )


class AddGoodRequest(BaseModel):
    """
    Add Good Request Schema.

    Defines the structure for adding a new good to the database.

    Attributes:
        name (str): The name of the good.
        price (float): The price of the good.
        count (int): The available quantity of the good.
        description (Optional[str]): A brief description of the good.
    """

    name: str = Field(
        ..., description="The name of the good."
    )
    price: float = Field(
        ..., description="The price of the good."
    )
    count: int = Field(
        ..., description="The available quantity of the good."
    )
    description: Optional[str] = Field(
        None, description="A brief description of the good."
    )

    class Config:
        """
        Configuration for the AddGoodRequest Schema.

        Provides example data for documentation purposes.
        """

        schema_extra = {
            "example": {
                "name": "Smartphone",
                "price": 699.99,
                "count": 50,
                "description": "A high-end smartphone with 128GB storage.",
            }
        }

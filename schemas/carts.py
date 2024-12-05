"""
Carts Schemas Module.

This module defines the Pydantic models related to shopping cart operations, including
cart creation, updating, deletion, and output representations. These schemas are used for
validating and serializing data in cart-related API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class CartItem(BaseModel):
    """
    Cart Item Schema.

    Defines the structure for individual items within a shopping cart.

    Attributes:
        product_id (str): The unique identifier of the product.
        quantity (int): The quantity of the product in the cart.
    """

    product_id: str = Field(
        ..., description="The unique identifier of the product."
    )
    quantity: int = Field(
        ..., description="The quantity of the product in the cart."
    )


class CartCreate(BaseModel):
    """
    Cart Creation Schema.

    Defines the structure for creating a new shopping cart.

    Attributes:
        items (List[CartItem]): A list of items to be included in the cart.
    """

    items: List[CartItem] = Field(
        ..., description="A list of items to be included in the cart."
    )


class CartUpdate(BaseModel):
    """
    Cart Update Schema.

    Defines the structure for updating an existing shopping cart.

    Attributes:
        items (List[CartItem]): A new list of items to replace the existing cart items.
    """

    items: List[CartItem] = Field(
        ..., description="A new list of items to replace the existing cart items."
    )


class CartOut(BaseModel):
    """
    Cart Output Schema.

    Defines the structure for the cart information returned by the API.

    Attributes:
        id (str): The unique identifier of the cart.
        user_id (str): The unique identifier of the user who owns the cart.
        items (List[CartItem]): A list of items in the cart.
    """

    id: str = Field(
        ..., description="The unique identifier of the cart."
    )
    user_id: str = Field(
        ..., description="The unique identifier of the user who owns the cart."
    )
    items: List[CartItem] = Field(
        ..., description="A list of items in the cart."
    )


class CartOutDelete(BaseModel):
    """
    Cart Deletion Confirmation Schema.

    Defines the structure for the confirmation message returned after deleting a cart.

    Attributes:
        id (str): The unique identifier of the deleted cart.
        status (str): The status message indicating successful deletion.
    """

    id: str = Field(
        ..., description="The unique identifier of the deleted cart."
    )
    status: str = Field(
        ..., description="The status message indicating successful deletion."
    )


class CartsOut(BaseModel):
    """
    Paginated Carts Output Schema.

    Defines the structure for a paginated list of carts returned by the API.

    Attributes:
        carts (List[CartOut]): A list of cart objects.
        page (int): The current page number.
        limit (int): The number of items per page.
    """

    carts: List[CartOut] = Field(
        ..., description="A list of cart objects."
    )
    page: int = Field(
        ..., description="The current page number."
    )
    limit: int = Field(
        ..., description="The number of items per page."
    )

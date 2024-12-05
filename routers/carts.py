"""
Carts Router Module.

This module defines the API endpoints related to shopping cart management, including
retrieving all carts, fetching a specific cart, creating a new cart, updating an existing
cart, and deleting a cart. It utilizes dependency injection for database access and user authentication.
"""

from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_database
from app.services.carts import CartService
from fastapi.security.http import HTTPAuthorizationCredentials
from app.schemas.carts import CartOut, CartUpdate, CartsOut, CartOutDelete
from app.core.security import security

router = APIRouter(tags=["Carts"], prefix="/carts")

@router.get("/", status_code=status.HTTP_200_OK, response_model=CartsOut)
async def get_all_carts(
        token: HTTPAuthorizationCredentials = Depends(security),
        db = Depends(get_database),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page")):
    """
    Retrieve All Shopping Carts.

    Fetches a paginated list of all shopping carts in the system.

    Args:
        token (HTTPAuthorizationCredentials): The JWT token for user authentication.
        db: The MongoDB database instance.
        page (int): The page number for pagination.
        limit (int): The number of items per page.

    Returns:
        CartsOut: A paginated list of shopping carts.
    """
    return await CartService.get_all_carts(token, db, page, limit)

@router.get("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
async def get_cart(
        cart_id: str,
        token: HTTPAuthorizationCredentials = Depends(security),
        db = Depends(get_database)):
    """
    Retrieve a Specific Shopping Cart by ID.

    Fetches the details of a single shopping cart identified by its ID.

    Args:
        cart_id (str): The unique identifier of the cart.
        token (HTTPAuthorizationCredentials): The JWT token for user authentication.
        db: The MongoDB database instance.

    Returns:
        CartOut: The details of the requested shopping cart.
    """
    return await CartService.get_cart(token, db, cart_id)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CartOut)
async def create_cart(
        cart_data: CartUpdate,
        token: HTTPAuthorizationCredentials = Depends(security),
        db = Depends(get_database)):
    """
    Create a New Shopping Cart.

    Creates a new shopping cart with the provided cart data.

    Args:
        cart_data (CartUpdate): The data for the new cart.
        token (HTTPAuthorizationCredentials): The JWT token for user authentication.
        db: The MongoDB database instance.

    Returns:
        CartOut: The details of the created shopping cart.
    """
    return await CartService.create_cart(token, db, cart_data)

@router.put("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
async def update_cart(
        cart_id: str,
        updated_cart: CartUpdate,
        token: HTTPAuthorizationCredentials = Depends(security),
        db = Depends(get_database)):
    """
    Update an Existing Shopping Cart.

    Updates the details of an existing shopping cart identified by its ID.

    Args:
        cart_id (str): The unique identifier of the cart to be updated.
        updated_cart (CartUpdate): The updated cart data.
        token (HTTPAuthorizationCredentials): The JWT token for user authentication.
        db: The MongoDB database instance.

    Returns:
        CartOut: The details of the updated shopping cart.
    """
    return await CartService.update_cart(token, db, cart_id, updated_cart)

@router.delete("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOutDelete)
async def delete_cart(
        cart_id: str,
        token: HTTPAuthorizationCredentials = Depends(security),
        db = Depends(get_database)):
    """
    Delete a Shopping Cart by ID.

    Permanently removes a shopping cart identified by its ID from the system.

    Args:
        cart_id (str): The unique identifier of the cart to be deleted.
        token (HTTPAuthorizationCredentials): The JWT token for user authentication.
        db: The MongoDB database instance.

    Returns:
        CartOutDelete: Confirmation details of the deleted shopping cart.
    """
    return await CartService.delete_cart(token, db, cart_id)

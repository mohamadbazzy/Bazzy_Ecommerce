# app/routers/carts.py

from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_database
from app.services.carts import CartService
from fastapi.security.http import HTTPAuthorizationCredentials
from app.schemas.carts import CartOut, CartUpdate, CartsOut, CartOutDelete
from app.core.security import security

router = APIRouter(tags=["Carts"], prefix="/carts")

# Get All Carts
@router.get("/", status_code=status.HTTP_200_OK, response_model=CartsOut)
async def get_all_carts(
        token: HTTPAuthorizationCredentials = Depends(security),
        db = Depends(get_database),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page")):
    return await CartService.get_all_carts(token, db, page, limit)

# Get Cart By ID
@router.get("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
async def get_cart(
        cart_id: str,
        token: HTTPAuthorizationCredentials = Depends(security),
        db = Depends(get_database)):
    return await CartService.get_cart(token, db, cart_id)

# Create New Cart
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CartOut)
async def create_cart(
        cart_data: CartUpdate,
        token: HTTPAuthorizationCredentials = Depends(security),
        db = Depends(get_database)):
    return await CartService.create_cart(token, db, cart_data)

# Update Existing Cart
@router.put("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
async def update_cart(
        cart_id: str,
        updated_cart: CartUpdate,
        token: HTTPAuthorizationCredentials = Depends(security),
        db = Depends(get_database)):
    return await CartService.update_cart(token, db, cart_id, updated_cart)

# Delete Cart By ID
@router.delete("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOutDelete)
async def delete_cart(
        cart_id: str,
        token: HTTPAuthorizationCredentials = Depends(security),
        db = Depends(get_database)):
    return await CartService.delete_cart(token, db, cart_id)

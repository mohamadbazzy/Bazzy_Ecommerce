# app/routers/products.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.products import ProductCreate, ProductOut, ProductUpdate
from app.services.products import ProductService
from app.db.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.security import check_admin_role, get_current_user
from app.models.user import UserModel  # Assuming you have a UserModel

router = APIRouter(
    tags=["Products"],
    prefix="/products"
)

# Create a New Product
@router.post(
    "/",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_admin_role)]
)
async def create_product(
    product: ProductCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    return await ProductService.create_product(db, product)

# Get All Products
@router.get(
    "/",
    response_model=List[ProductOut],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_admin_role)]
)
async def get_all_products(
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    return await ProductService.get_all_products(db)

# Get Product By ID
@router.get(
    "/{product_id}",
    response_model=ProductOut,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_admin_role)]
)
async def get_product(
    product_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    return await ProductService.get_product(db, product_id)

# Update Existing Product
@router.patch(
    "/{product_id}",
    response_model=ProductOut,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_admin_role)]
)
async def update_product(
    product_id: str,
    updated_product: ProductUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    return await ProductService.update_product(db, product_id, updated_product)

# Delete Product By ID
@router.delete(
    "/{product_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_admin_role)]
)
async def delete_product(
    product_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    await ProductService.delete_product(db, product_id)
    return {"detail": f"Product with ID '{product_id}' has been deleted."}

"""
Products Router Module.

This module defines the API endpoints related to product management, including
creating new products, retrieving all products, fetching a specific product, updating
an existing product, and deleting a product. Administrative privileges are required for
creating, updating, and deleting products.
"""

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
    """
    Create a New Product.

    Adds a new product to the database with the provided product data. Requires administrative privileges.

    Args:
        product (ProductCreate): The data for the new product.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        ProductOut: The details of the created product.
    """
    return await ProductService.create_product(db, product)

@router.get(
    "/",
    response_model=List[ProductOut],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_admin_role)]
)
async def get_all_products(
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Retrieve All Products.

    Fetches a list of all products available in the system. Requires administrative privileges.

    Args:
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        List[ProductOut]: A list of all products.
    """
    return await ProductService.get_all_products(db)

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
    """
    Retrieve a Specific Product by ID.

    Fetches the details of a single product identified by its ID. Requires administrative privileges.

    Args:
        product_id (str): The unique identifier of the product.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        ProductOut: The details of the requested product.
    """
    return await ProductService.get_product(db, product_id)

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
    """
    Update an Existing Product.

    Updates the details of an existing product identified by its ID. Requires administrative privileges.

    Args:
        product_id (str): The unique identifier of the product to be updated.
        updated_product (ProductUpdate): The updated product data.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        ProductOut: The details of the updated product.
    """
    return await ProductService.update_product(db, product_id, updated_product)

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
    """
    Delete a Product by ID.

    Permanently removes a product identified by its ID from the system. Requires administrative privileges.

    Args:
        product_id (str): The unique identifier of the product to be deleted.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        dict: A confirmation message indicating successful deletion.
    """
    await ProductService.delete_product(db, product_id)
    return {"detail": f"Product with ID '{product_id}' has been deleted."}

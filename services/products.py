"""
Products Service Module.

This module defines the `ProductService` class, which manages product-related
operations such as creating new products, retrieving all products, fetching a specific
product, updating an existing product, and deleting a product. It interacts with the
database to perform CRUD operations on product data.
"""

from app.schemas.products import ProductCreate, ProductOut, ProductUpdate
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from fastapi import HTTPException, status
from typing import List


class ProductService:
    """
    Service class for managing products.
    """

    @staticmethod
    async def create_product(db: AsyncIOMotorDatabase, product: ProductCreate) -> ProductOut:
        """
        Create a new product.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            product (ProductCreate): The product data to be created.

        Returns:
            ProductOut: The created product details.

        Raises:
            HTTPException: If the product creation fails.
        """
        product_dict = product.dict()
        result = await db["products"].insert_one(product_dict)
        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create product."
            )
        product_dict["_id"] = result.inserted_id
        return ProductOut(**product_dict)
    
    @staticmethod
    async def get_all_products(db: AsyncIOMotorDatabase) -> List[ProductOut]:
        """
        Retrieve all products.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.

        Returns:
            List[ProductOut]: A list of all products.
        """
        products_cursor = db["products"].find()
        products = []
        async for product in products_cursor:
            product_out = ProductOut(**product)
            products.append(product_out)
        return products
    
    @staticmethod
    async def get_product(db: AsyncIOMotorDatabase, product_id: str) -> ProductOut:
        """
        Retrieve a specific product by its ID.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            product_id (str): The unique identifier of the product.

        Returns:
            ProductOut: The product details.

        Raises:
            HTTPException: If the product ID format is invalid or the product is not found.
        """
        if not ObjectId.is_valid(product_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid product ID format."
            )
        product = await db["products"].find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID '{product_id}' not found."
            )
        return ProductOut(**product)
    
    @staticmethod
    async def update_product(db: AsyncIOMotorDatabase, product_id: str, updated_product: ProductUpdate) -> ProductOut:
        """
        Update an existing product.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            product_id (str): The unique identifier of the product to be updated.
            updated_product (ProductUpdate): The updated product data.

        Returns:
            ProductOut: The updated product details.

        Raises:
            HTTPException: If the product ID format is invalid, no fields are provided for update,
                           or the product is not found.
        """
        if not ObjectId.is_valid(product_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid product ID format."
            )
        update_data = {k: v for k, v in updated_product.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update."
            )
        result = await db["products"].update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID '{product_id}' not found."
            )
        product = await db["products"].find_one({"_id": ObjectId(product_id)})
        return ProductOut(**product)
    
    @staticmethod
    async def delete_product(db: AsyncIOMotorDatabase, product_id: str) -> None:
        """
        Delete a product by its ID.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            product_id (str): The unique identifier of the product to be deleted.

        Raises:
            HTTPException: If the product ID format is invalid or the product is not found.
        """
        if not ObjectId.is_valid(product_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid product ID format."
            )
        result = await db["products"].delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID '{product_id}' not found."
            )

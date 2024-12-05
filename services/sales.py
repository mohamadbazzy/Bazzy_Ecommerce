"""
Sales Service Module.

This module defines the `SalesService` class, which manages sales operations such as
displaying available goods, retrieving details of specific goods, processing sales
transactions, and adding new goods to the database. It interacts with the database to
perform CRUD operations on sales and goods data.
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.schemas.sales import SaleRequest, SaleResponse, AddGoodRequest


class SalesService:
    """
    Service class for managing sales operations.
    """

    @staticmethod
    async def get_goods(db: AsyncIOMotorDatabase):
        """
        Fetch all available goods that are in stock.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.

        Returns:
            list: A list of dictionaries containing good names and prices.
        """
        goods = await db["goods"].find({"count": {"$gt": 0}}).to_list(length=100)
        return [{"name": good["name"], "price": good["price"]} for good in goods]

    @staticmethod
    async def get_good_details(db: AsyncIOMotorDatabase, good_name: str):
        """
        Retrieve detailed information about a specific good.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            good_name (str): The name of the good.

        Returns:
            dict: A dictionary containing good details.

        Raises:
            HTTPException: If the good is not found.
        """
        good = await db["goods"].find_one({"name": good_name})
        if not good:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Good not found"
            )
        return {
            "name": good["name"],
            "price": good["price"],
            "description": good.get("description", ""),
            "count": good["count"],
        }

    @staticmethod
    async def process_sale(db: AsyncIOMotorDatabase, sale_request: SaleRequest) -> SaleResponse:
        """
        Process a sale transaction if conditions are met.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            sale_request (SaleRequest): The sale request data.

        Returns:
            SaleResponse: A Pydantic model containing the sale response details.

        Raises:
            HTTPException: If the good is not available, the user is not found,
                           insufficient balance, or the good is out of stock.
        """
        # Fetch good details
        good = await db["goods"].find_one({"name": sale_request.good_name})
        if not good:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Good not available"
            )

        # Fetch user wallet
        user = await db["users"].find_one({"username": sale_request.username})
        if not user or user["wallet"]["balance"] < good["price"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance or user not found",
            )

        # Check if good is in stock
        if good["count"] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Good is out of stock"
            )

        # Deduct price from wallet and reduce stock
        new_balance = user["wallet"]["balance"] - good["price"]
        await db["users"].update_one(
            {"username": sale_request.username}, {"$set": {"wallet.balance": new_balance}}
        )
        await db["goods"].update_one(
            {"name": sale_request.good_name}, {"$inc": {"count": -1}}
        )

        # Save purchase history
        purchase = {
            "username": sale_request.username,
            "good_name": sale_request.good_name,
            "price": good["price"],
        }
        await db["purchases"].insert_one(purchase)

        return SaleResponse(
            message="Purchase successful",
            remaining_balance=new_balance,
            purchased_item=sale_request.good_name,
        )

    @staticmethod
    async def add_good(db: AsyncIOMotorDatabase, good: AddGoodRequest):
        """
        Add a new good to the database.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            good (AddGoodRequest): The good data to be added.

        Raises:
            HTTPException: If the good already exists.
        """
        # Check if the good already exists
        existing_good = await db["goods"].find_one({"name": good.name})
        if existing_good:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Good already exists"
            )
        
        # Insert the good
        new_good = {
            "name": good.name,
            "price": good.price,
            "count": good.count,
            "description": good.description
        }
        await db["goods"].insert_one(new_good)

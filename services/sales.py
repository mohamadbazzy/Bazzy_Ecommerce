from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.schemas.sales import SaleRequest, SaleResponse

class SalesService:
    @staticmethod
    async def get_goods(db: AsyncIOMotorDatabase):
        """Fetch available goods"""
        goods = await db["goods"].find({"count": {"$gt": 0}}).to_list(length=100)
        return [{"name": good["name"], "price": good["price"]} for good in goods]

    @staticmethod
    async def get_good_details(db: AsyncIOMotorDatabase, good_name: str):
        """Fetch details of a specific good"""
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
    async def process_sale(db: AsyncIOMotorDatabase, sale_request: SaleRequest):
        """Process a sale if conditions are met"""
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

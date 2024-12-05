from app.schemas.users import UserCreate, UserOut, UserUpdate, UserOutDelete, Wallet, UsersOut
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from fastapi import HTTPException, status
from typing import List, Optional
from app.core.security import get_password_hash


class UserService:
    @staticmethod
    async def create_user(db: AsyncIOMotorDatabase, user_data: UserCreate) -> UserOut:
        # Check if username or email already exists
        existing_user = await db["users"].find_one({
            "$or": [
                {"username": user_data.username},
                {"email": user_data.email}
            ]
        })
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists."
            )
        
        # Hash the password
        hashed_password = get_password_hash(user_data.password)
        
        # Prepare the user document
        user_dict = user_data.dict(exclude_unset=True)
        user_dict["hashed_password"] = hashed_password
        user_dict.pop("password", None)  # Remove plain password
        
        # Insert the user into the database
        result = await db["users"].insert_one(user_dict)
        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user."
            )
        
        # Optionally, create a wallet for the user
        wallet = {
            "user_id": str(result.inserted_id),
            "balance": 0.0,
            "transactions": []
        }
        wallet_result = await db["wallets"].insert_one(wallet)
        if not wallet_result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create wallet."
            )
        
        # Fetch the newly created user with wallet
        new_user = await db["users"].find_one({"_id": result.inserted_id})
        if new_user:
            wallet_data = await db["wallets"].find_one({"user_id": str(result.inserted_id)})
            if wallet_data:
                wallet_data["id"] = str(wallet_data["_id"])  # Add the `id` field from `_id`
                wallet_data.pop("_id", None)  # Remove `_id` for consistency
            new_user["wallet"] = wallet_data
            new_user["id"] = str(new_user["_id"])  # Convert `_id` to `id`
            new_user.pop("_id", None)  # Remove `_id` for consistency
            return UserOut(**new_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve created user."
            )

    @staticmethod
    async def get_all_users(db: AsyncIOMotorDatabase, page: int, limit: int, search: str, role: str) -> UsersOut:
        skip = (page - 1) * limit
        query = {}
        if search:
            query["username"] = {"$regex": search, "$options": "i"}  # Case-insensitive search
        if role:
            query["role"] = role
        
        cursor = db["users"].find(query).skip(skip).limit(limit)
        users = []
        async for user in cursor:
            # Fetch wallet, or use a default wallet if not found
            wallet = await db["wallets"].find_one({"user_id": str(user["_id"])})
            if wallet:
                wallet["id"] = str(wallet["_id"])
                wallet.pop("_id", None)
            else:
                wallet = {"id": None, "balance": 0.0, "transactions": []}  # Default wallet
            
            user["wallet"] = wallet
            user["id"] = str(user["_id"])
            user.pop("_id", None)
            users.append(UserOut(**user))
        
        total = await db["users"].count_documents(query)
        return UsersOut(users=users, total=total, page=page, limit=limit)

    
    @staticmethod
    async def get_user(db: AsyncIOMotorDatabase, user_id: str) -> UserOut:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format."
            )
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID '{user_id}' not found."
            )
        wallet = await db["wallets"].find_one({"user_id": str(user["_id"])})
        if wallet:
            wallet["id"] = str(wallet["_id"])
            wallet.pop("_id", None)
        user["wallet"] = wallet
        user["id"] = str(user["_id"])
        user.pop("_id", None)
        return UserOut(**user)
    
    @staticmethod
    async def update_user(db: AsyncIOMotorDatabase, user_id: str, updated_user: UserUpdate) -> UserOut:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format."
            )
        obj_id = ObjectId(user_id)
        
        # Prepare the update data
        update_data = updated_user.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update."
            )
        
        # Update the user document
        result = await db["users"].update_one({"_id": obj_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID '{user_id}' not found."
            )
        
        # Fetch the updated user
        user = await db["users"].find_one({"_id": obj_id})
        wallet = await db["wallets"].find_one({"user_id": str(user["_id"])})
        if wallet:
            wallet["id"] = str(wallet["_id"])
            wallet.pop("_id", None)
        user["wallet"] = wallet
        user["id"] = str(user["_id"])
        user.pop("_id", None)
        return UserOut(**user)
    
    @staticmethod
    async def delete_user(db: AsyncIOMotorDatabase, user_id: str) -> UserOutDelete:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format."
            )
        obj_id = ObjectId(user_id)
        
        # Find the user
        user = await db["users"].find_one({"_id": obj_id})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID '{user_id}' not found."
            )
        
        # Delete the user
        await db["users"].delete_one({"_id": obj_id})
        # Delete the associated wallet
        await db["wallets"].delete_one({"user_id": str(obj_id)})
        
        return UserOutDelete(
            id=str(user["_id"]),
            username=user["username"],
            email=user["email"],
            role=user["role"]
        )
    
    @staticmethod
    async def add_wallet(db: AsyncIOMotorDatabase, user_id: str, amount: float) -> None:
        wallet = await db["wallets"].find_one({"user_id": user_id})
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wallet for user ID '{user_id}' not found."
            )
        new_balance = wallet.get("balance", 0.0) + amount
        await db["wallets"].update_one(
            {"user_id": user_id},
            {"$set": {"balance": new_balance}}
        )
    
    @staticmethod
    async def deduct_wallet(db: AsyncIOMotorDatabase, user_id: str, amount: float) -> None:
        wallet = await db["wallets"].find_one({"user_id": user_id})
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wallet for user ID '{user_id}' not found."
            )
        current_balance = wallet.get("balance", 0.0)
        if current_balance < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance."
            )
        new_balance = current_balance - amount
        await db["wallets"].update_one(
            {"user_id": user_id},
            {"$set": {"balance": new_balance}}
        )

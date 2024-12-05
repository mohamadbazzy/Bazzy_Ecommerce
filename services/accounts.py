"""
Accounts Service Module.

This module defines the `AccountService` class, which encapsulates the business logic
related to user account management, including retrieving account information, updating
account details, and deleting user accounts. It interacts with the database to perform
CRUD operations on account data.
"""

from app.core.security import get_current_user
from app.schemas.accounts import AccountUpdate
from bson import ObjectId
from fastapi import HTTPException


class AccountService:
    """
    Service class for managing user accounts.
    """

    @staticmethod
    async def get_my_info(db, token):
        """
        Retrieve the authenticated user's account information.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            token: The JWT token containing user credentials.

        Returns:
            dict: A dictionary containing the user's account details.

        Raises:
            HTTPException: If the account is not found.
        """
        user = await get_current_user(token)
        account = await db["accounts"].find_one({"user_id": ObjectId(user["_id"])})
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        account["id"] = str(account["_id"])
        account["user_id"] = str(account["user_id"])
        return account

    @staticmethod
    async def edit_my_info(db, token, updated_account: AccountUpdate):
        """
        Update the authenticated user's account information.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            token: The JWT token containing user credentials.
            updated_account (AccountUpdate): The updated account information.

        Returns:
            dict: A dictionary containing the updated account details.

        Raises:
            HTTPException: If the account is not found or not modified.
        """
        user = await get_current_user(token)
        update_data = updated_account.dict(exclude_unset=True)
        result = await db["accounts"].update_one(
            {"user_id": ObjectId(user["_id"])},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Account not found or not modified")
        return await AccountService.get_my_info(db, token)

    @staticmethod
    async def remove_my_account(db, token):
        """
        Delete the authenticated user's account.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            token: The JWT token containing user credentials.

        Returns:
            dict: A confirmation dictionary indicating successful deletion.

        Raises:
            HTTPException: If the account is not found.
        """
        user = await get_current_user(token)
        result = await db["accounts"].delete_one({"user_id": ObjectId(user["_id"])})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Account not found")
        return {"id": str(user["_id"]), "status": "deleted"}

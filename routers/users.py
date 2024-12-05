"""
Users Router Module.

This module defines the API endpoints related to user management, including creating new users,
retrieving user information, updating user details, deleting users, and managing wallet transactions.
Administrative privileges are required for certain operations to ensure secure and authorized access.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.users import (
    UserCreate, UserOut, UsersOut, UserOutDelete,
    UserUpdate, WalletTransaction
)
from app.services.users import UserService
from app.db.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.security import check_admin_role, get_current_user
from app.models.user import UserModel  # Assuming you have a UserModel

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)

@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_admin_role)]
)
async def create_user(
    user: UserCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Create a New User.

    Registers a new user with the provided user creation data. Requires administrative privileges.

    Args:
        user (UserCreate): The data for the new user.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        UserOut: The created user's information.
    """
    return await UserService.create_user(db, user)

@router.get(
    "/",
    response_model=UsersOut,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_admin_role)]
)
async def get_all_users(
    db: AsyncIOMotorDatabase = Depends(get_database),
    page: int = 1,
    limit: int = 10,
    search: str = "",
    role: str = "user"
):
    """
    Retrieve All Users.

    Fetches a paginated list of all users, with optional filtering based on search query and role.
    Requires administrative privileges.

    Args:
        db (AsyncIOMotorDatabase): The MongoDB database instance.
        page (int): The page number for pagination.
        limit (int): The number of users per page.
        search (str): The search query to filter users by name or other attributes.
        role (str): The role to filter users by (e.g., "admin", "user").

    Returns:
        UsersOut: A paginated list of users.
    """
    return await UserService.get_all_users(db, page, limit, search, role)

@router.get(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_admin_role)]
)
async def get_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Retrieve a Specific User by ID.

    Fetches the details of a single user identified by their ID. Requires administrative privileges.

    Args:
        user_id (str): The unique identifier of the user.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        UserOut: The details of the requested user.
    """
    return await UserService.get_user(db, user_id)

@router.patch(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_admin_role)]
)
async def update_user(
    user_id: str,
    updated_user: UserUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Update an Existing User.

    Updates the details of an existing user identified by their ID. Requires administrative privileges.

    Args:
        user_id (str): The unique identifier of the user to be updated.
        updated_user (UserUpdate): The updated user data.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        UserOut: The details of the updated user.
    """
    return await UserService.update_user(db, user_id, updated_user)

@router.delete(
    "/{user_id}",
    response_model=UserOutDelete,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_admin_role)]
)
async def delete_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Delete a User by ID.

    Permanently removes a user identified by their ID from the system. Requires administrative privileges.

    Args:
        user_id (str): The unique identifier of the user to be deleted.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        UserOutDelete: Confirmation details of the deleted user.
    """
    return await UserService.delete_user(db, user_id)

@router.post(
    "/{user_id}/wallet/add",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_admin_role)]
)
async def add_to_wallet(
    user_id: str,
    transaction: WalletTransaction,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Add Funds to User's Wallet.

    Adds a specified amount to the user's wallet. Requires administrative privileges.

    Args:
        user_id (str): The unique identifier of the user.
        transaction (WalletTransaction): The transaction details, including the amount to add.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        UserOut: The updated user information with the new wallet balance.
    """
    await UserService.add_wallet(db, user_id, transaction.amount)
    return await UserService.get_user(db, user_id)

@router.post(
    "/{user_id}/wallet/deduct",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_admin_role)]
)
async def deduct_from_wallet(
    user_id: str,
    transaction: WalletTransaction,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Deduct Funds from User's Wallet.

    Deducts a specified amount from the user's wallet. Requires administrative privileges.

    Args:
        user_id (str): The unique identifier of the user.
        transaction (WalletTransaction): The transaction details, including the amount to deduct.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        UserOut: The updated user information with the new wallet balance.
    """
    await UserService.deduct_wallet(db, user_id, transaction.amount)
    return await UserService.get_user(db, user_id)

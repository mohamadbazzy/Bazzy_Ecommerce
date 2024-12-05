# app/routers/users.py

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

# Create New User
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
    return await UserService.create_user(db, user)

# Get All Users
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
    return await UserService.get_all_users(db, page, limit, search, role)

# Get User By ID
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
    return await UserService.get_user(db, user_id)

# Update Existing User
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
    return await UserService.update_user(db, user_id, updated_user)

# Delete User By ID
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
    return await UserService.delete_user(db, user_id)

# Add to Wallet
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
    await UserService.add_wallet(db, user_id, transaction.amount)
    return await UserService.get_user(db, user_id)

# Deduct from Wallet
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
    await UserService.deduct_wallet(db, user_id, transaction.amount)
    return await UserService.get_user(db, user_id)

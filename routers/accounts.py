"""
Accounts Router Module.

This module defines the API endpoints related to user account management, such as retrieving
user information, updating account details, and deleting user accounts. It utilizes dependency
injection to access the database and authenticate users.
"""

from fastapi import APIRouter, Depends
from app.db.database import get_db
from app.services.accounts import AccountService
from app.schemas.accounts import AccountOut, AccountUpdate
from fastapi.security.http import HTTPAuthorizationCredentials
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user
)

router = APIRouter(tags=["Account"], prefix="/me")

@router.get("/", response_model=AccountOut)
async def get_my_info(
        db = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(get_current_user)):
    """
    Retrieve Current User Information.

    Fetches the authenticated user's account information from the database.

    Args:
        db: The MongoDB database instance.
        token (HTTPAuthorizationCredentials): The JWT token containing user credentials.

    Returns:
        AccountOut: The user's account details.
    """
    return await AccountService.get_my_info(db, token)

@router.put("/", response_model=AccountOut)
async def edit_my_info(
        updated_user: AccountUpdate,
        db = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(get_current_user)):
    """
    Update Current User Information.

    Allows the authenticated user to update their account details.

    Args:
        updated_user (AccountUpdate): The updated account information provided by the user.
        db: The MongoDB database instance.
        token (HTTPAuthorizationCredentials): The JWT token containing user credentials.

    Returns:
        AccountOut: The updated user's account details.
    """
    return await AccountService.edit_my_info(db, token, updated_user)

@router.delete("/", response_model=AccountOut)
async def remove_my_account(
        db = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(get_current_user)):
    """
    Delete Current User Account.

    Permanently removes the authenticated user's account from the database.

    Args:
        db: The MongoDB database instance.
        token (HTTPAuthorizationCredentials): The JWT token containing user credentials.

    Returns:
        AccountOut: The details of the deleted user account.
    """
    return await AccountService.remove_my_account(db, token)

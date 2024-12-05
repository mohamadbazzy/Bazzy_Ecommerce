"""
Authentication Router Module.

This module defines the API endpoints related to user authentication, including user signup,
login, and token refreshing. It handles the creation and validation of JWT tokens for secure access.
"""

from typing import Optional, List, Dict

from fastapi import APIRouter, Depends, status, Header
from app.services.auth import AuthService
from app.db.database import get_database
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.schemas.auth import UserOut, Signup
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(tags=["Auth"], prefix="/auth")

@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def user_signup(user: Signup, db: AsyncIOMotorClient = Depends(get_database)):
    """
    User Signup Endpoint.

    Registers a new user by creating an account with the provided signup information.

    Args:
        user (Signup): The signup information provided by the user.
        db (AsyncIOMotorClient): The MongoDB database instance.

    Returns:
        UserOut: The created user's information.
    """
    return await AuthService.signup(db, user)

@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db = Depends(get_database)):
    """
    User Login Endpoint.

    Authenticates a user using their credentials and returns a JWT token upon successful authentication.

    Args:
        user_credentials (OAuth2PasswordRequestForm): The user's login credentials.
        db: The MongoDB database instance.

    Returns:
        Dict[str, str]: A dictionary containing the access token and token type.
    """
    return await AuthService.login(user_credentials, db)

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(
        refresh_token: str = Header(..., description="Refresh token for obtaining a new access token"),
        db = Depends(get_database)):
    """
    Refresh Access Token Endpoint.

    Generates a new access token using a valid refresh token.

    Args:
        refresh_token (str): The refresh token provided in the request header.
        db: The MongoDB database instance.

    Returns:
        Dict[str, str]: A dictionary containing the new access token and token type.
    """
    return await AuthService.get_refresh_token(token=refresh_token, db=db)

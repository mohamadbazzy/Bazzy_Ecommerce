"""
Authentication Service Module.

This module defines the `AuthService` class, which handles user authentication
operations such as user signup, login, and token refreshing. It interacts with the
database to manage user credentials and generate JWT tokens for secure access.
"""

from fastapi import HTTPException, status
from app.schemas.auth import Token, Signup, UserInDB
from app.core.security import verify_password, create_access_token, get_password_hash
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


class AuthService:
    """
    Service class for handling authentication-related operations.
    """

    @staticmethod
    async def signup(db: AsyncIOMotorClient, user: Signup):
        """
        Register a new user.

        Args:
            db (AsyncIOMotorClient): The MongoDB database instance.
            user (Signup): The signup information provided by the user.

        Returns:
            dict: A dictionary containing the created user's information.

        Raises:
            HTTPException: If the username or email already exists.
        """
        # Check if username or email already exists
        existing_user = await db["users"].find_one({
            "$or": [
                {"username": user.username},
                {"email": user.email}
            ]
        })
        if existing_user:
            if existing_user["username"] == user.username:
                raise HTTPException(status_code=400, detail="Username already taken")
            else:
                raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash the password
        hashed_password = get_password_hash(user.password)
        
        # Prepare user data
        user_dict = user.dict()
        user_dict["hashed_password"] = hashed_password
        user_dict.pop("password")  # Remove plain password
        
        # Insert the user into the database
        result = await db["users"].insert_one(user_dict)
        user_dict["_id"] = result.inserted_id
        user_dict["id"] = str(user_dict["_id"])
        user_dict.pop("_id")
        user_dict.pop("hashed_password")  # Exclude hashed password from the response
        
        return user_dict

    @staticmethod
    async def login(user_credentials: OAuth2PasswordRequestForm, db: AsyncIOMotorClient) -> Token:
        """
        Authenticate a user and generate a JWT token.

        Args:
            user_credentials (OAuth2PasswordRequestForm): The user's login credentials.
            db (AsyncIOMotorClient): The MongoDB database instance.

        Returns:
            Token: A Pydantic model containing the access token and token type.

        Raises:
            HTTPException: If the username or password is incorrect.
        """
        user = await db["users"].find_one({"username": user_credentials.username})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(user_credentials.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(
            data={"sub": user["username"], "role": user["role"]}
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def get_refresh_token(token: str, db: AsyncIOMotorClient) -> Token:
        """
        Refresh the access token using a refresh token.

        Args:
            token (str): The refresh token provided in the request header.
            db (AsyncIOMotorClient): The MongoDB database instance.

        Returns:
            Token: A Pydantic model containing the new access token and token type.

        Raises:
            HTTPException: If the refresh token functionality is not implemented.
        """
        # Implement refresh token logic here
        # Placeholder implementation
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Refresh token functionality not implemented yet."
        )

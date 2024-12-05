from fastapi import HTTPException, status
from app.schemas.auth import Token, Signup, UserInDB
from app.core.security import verify_password, create_access_token, get_password_hash
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

class AuthService:

    @staticmethod
    async def signup(db: AsyncIOMotorClient, user: Signup):
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
        # Implement refresh token logic here
        # Placeholder implementation
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Refresh token functionality not implemented yet."
        )

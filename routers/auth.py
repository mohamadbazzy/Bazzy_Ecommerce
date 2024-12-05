# app/routers/auth.py
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
    return await AuthService.signup(db, user)

@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db = Depends(get_database)):
    return await AuthService.login(user_credentials, db)

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(
        refresh_token: str = Header(),
        db = Depends(get_database)):
    return await AuthService.get_refresh_token(token=refresh_token, db=db)

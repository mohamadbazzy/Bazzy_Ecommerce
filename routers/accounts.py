# app/routers/accounts.py

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
    return await AccountService.get_my_info(db, token)

@router.put("/", response_model=AccountOut)
async def edit_my_info(
        updated_user: AccountUpdate,
        db = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(get_current_user)):
    return await AccountService.edit_my_info(db, token, updated_user)

@router.delete("/", response_model=AccountOut)
async def remove_my_account(
        db = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(get_current_user)):
    return await AccountService.remove_my_account(db, token)

from pydantic import BaseModel, Field
from typing import Optional

class AccountCreate(BaseModel):
    address: Optional[str]
    phone_number: Optional[str]

class AccountUpdate(BaseModel):
    address: Optional[str]
    phone_number: Optional[str]

class AccountOut(BaseModel):
    id: str
    user_id: str
    address: Optional[str]
    phone_number: Optional[str]

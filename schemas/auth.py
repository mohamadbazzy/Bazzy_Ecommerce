from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class Signup(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"

class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: str

class UserInDB(UserOut):
    hashed_password: str

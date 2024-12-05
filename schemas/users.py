from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class Wallet(BaseModel):
    id: Optional[str]  # `id` is optional to avoid validation issues
    balance: float = 0.0
    transactions: Optional[List] = []  # Adjust based on actual wallet structure

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "wallet_id",
                "balance": 100.0,
                "transactions": []
            }
        }


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: str = Field("user", description="Role of the user: 'user' or 'admin'")
    age: Optional[int] = Field(None, ge=0, le=150, description="Age of the user")
    gender: Optional[str] = Field(None, description="Gender of the user")
    address: Optional[str] = Field(None, description="Address of the user")
    marital_status: Optional[str] = Field(None, description="Marital status of the user")

    class Config:
        schema_extra = {
            "example": {
                "username": "Mohamad",
                "email": "mab13401@mail.com",
                "role": "user",
                "age": 30,
                "gender": "Male",
                "address": "123 Main Street, Beirut",
                "marital_status": "Single"
            }
        }


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Plain-text password")

    class Config:
        schema_extra = {
            "example": {
                "username": "Mohamad",
                "email": "mab13401@mail.com",
                "password": "your_secure_password",
                "role": "user",
                "age": 30,
                "gender": "Male",
                "address": "123 Main Street, Beirut",
                "marital_status": "Single"
            }
        }


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, description="New plain-text password")
    role: Optional[str] = Field(None, description="Role of the user: 'user' or 'admin'")
    age: Optional[int] = Field(None, ge=0, le=150, description="Age of the user")
    gender: Optional[str] = Field(None, description="Gender of the user")
    address: Optional[str] = Field(None, description="Address of the user")
    marital_status: Optional[str] = Field(None, description="Marital status of the user")

    class Config:
        schema_extra = {
            "example": {
                "email": "new_email@example.com",
                "password": "NewSecurePass123!",
                "age": 31,
                "gender": "Male",
                "address": "456 Another Street, Beirut",
                "marital_status": "Married"
            }
        }


class UserOut(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    wallet: Optional[Wallet] = None  # Wallet is optional to fix validation error

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "user_id",
                "username": "Mohamad",
                "email": "mab13401@mail.com",
                "role": "user",
                "age": 30,
                "gender": "Male",
                "address": "123 Main Street, Beirut",
                "marital_status": "Single",
                "wallet": {
                    "id": "wallet_id",
                    "balance": 100.0,
                    "transactions": []
                }
            }
        }


class UsersOut(BaseModel):
    users: List[UserOut]
    total: int
    page: int
    limit: int

    class Config:
        schema_extra = {
            "example": {
                "users": [
                    {
                        "id": "user_id",
                        "username": "Mohamad",
                        "email": "mab13401@mail.com",
                        "role": "user",
                        "age": 30,
                        "gender": "Male",
                        "address": "123 Main Street, Beirut",
                        "marital_status": "Single",
                        "wallet": {
                            "id": "wallet_id",
                            "balance": 100.0,
                            "transactions": []
                        }
                    }
                ],
                "total": 1,
                "page": 1,
                "limit": 10
            }
        }


class UserOutDelete(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: str

    class Config:
        schema_extra = {
            "example": {
                "id": "user_id",
                "username": "Mohamad",
                "email": "mab13401@mail.com",
                "role": "user"
            }
        }


class WalletTransaction(BaseModel):
    amount: float

    class Config:
        schema_extra = {
            "example": {
                "amount": 50.0
            }
        }

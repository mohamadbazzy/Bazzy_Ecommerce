"""
Users Schemas Module.

This module defines the Pydantic models related to user management, including
user creation, updating, wallet transactions, and output representations. These schemas are used for
validating and serializing data in user-related API endpoints.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from bson import ObjectId


class PyObjectId(ObjectId):
    """
    Custom PyObjectId Type.

    Extends MongoDB's `ObjectId` to integrate seamlessly with Pydantic models,
    enabling validation and serialization of ObjectId fields.
    """

    @classmethod
    def __get_validators__(cls):
        """
        Yield validator functions for Pydantic.

        Yields:
            Callable: The validator method for `PyObjectId`.
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """
        Validate and convert input to an `ObjectId`.

        Args:
            v (str | ObjectId): The value to validate and convert.

        Returns:
            ObjectId: The validated `ObjectId`.

        Raises:
            ValueError: If the input is not a valid `ObjectId`.
        """
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class Wallet(BaseModel):
    """
    Wallet Schema.

    Defines the structure for a user's wallet.

    Attributes:
        id (Optional[str]): The unique identifier of the wallet.
        balance (float): The current balance in the wallet.
        transactions (Optional[List]): A list of transactions associated with the wallet.
    """

    id: Optional[str] = Field(
        None, description="The unique identifier of the wallet."
    )
    balance: float = Field(
        0.0, description="The current balance in the wallet."
    )
    transactions: Optional[List] = Field(
        [], description="A list of transactions associated with the wallet."
    )
    # Adjust based on actual wallet structure

    class Config:
        """
        Configuration for the Wallet Schema.

        Provides example data for documentation purposes.
        """

        orm_mode = True
        schema_extra = {
            "example": {
                "id": "wallet_id",
                "balance": 100.0,
                "transactions": []
            }
        }


class UserBase(BaseModel):
    """
    Base User Schema.

    Defines the common structure for user-related operations.

    Attributes:
        username (str): The username of the user.
        email (EmailStr): The email address of the user.
        role (str): The role of the user (e.g., "user", "admin").
        age (Optional[int]): The age of the user.
        gender (Optional[str]): The gender of the user.
        address (Optional[str]): The address of the user.
        marital_status (Optional[str]): The marital status of the user.
    """

    username: str = Field(
        ..., min_length=3, max_length=50, description="The username of the user."
    )
    email: EmailStr = Field(
        ..., description="The email address of the user."
    )
    role: str = Field(
        "user", description="Role of the user: 'user' or 'admin'."
    )
    age: Optional[int] = Field(
        None, ge=0, le=150, description="Age of the user."
    )
    gender: Optional[str] = Field(
        None, description="Gender of the user."
    )
    address: Optional[str] = Field(
        None, description="Address of the user."
    )
    marital_status: Optional[str] = Field(
        None, description="Marital status of the user."
    )

    class Config:
        """
        Configuration for the UserBase Schema.

        Provides example data for documentation purposes.
        """

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
    """
    User Creation Schema.

    Defines the structure for creating a new user.

    Attributes:
        password (str): The plain-text password for the user.
    """

    password: str = Field(
        ..., min_length=6, description="Plain-text password."
    )

    class Config:
        """
        Configuration for the UserCreate Schema.

        Provides example data for documentation purposes.
        """

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
    """
    User Update Schema.

    Defines the structure for updating an existing user.

    Attributes:
        username (Optional[str]): The new username of the user.
        email (Optional[EmailStr]): The new email address of the user.
        password (Optional[str]): The new plain-text password for the user.
        role (Optional[str]): The new role of the user.
        age (Optional[int]): The new age of the user.
        gender (Optional[str]): The new gender of the user.
        address (Optional[str]): The new address of the user.
        marital_status (Optional[str]): The new marital status of the user.
    """

    username: Optional[str] = Field(
        None, min_length=3, max_length=50, description="The new username of the user."
    )
    email: Optional[EmailStr] = Field(
        None, description="The new email address of the user."
    )
    password: Optional[str] = Field(
        None, min_length=6, description="New plain-text password."
    )
    role: Optional[str] = Field(
        None, description="The new role of the user."
    )
    age: Optional[int] = Field(
        None, ge=0, le=150, description="The new age of the user."
    )
    gender: Optional[str] = Field(
        None, description="The new gender of the user."
    )
    address: Optional[str] = Field(
        None, description="The new address of the user."
    )
    marital_status: Optional[str] = Field(
        None, description="The new marital status of the user."
    )

    class Config:
        """
        Configuration for the UserUpdate Schema.

        Provides example data for documentation purposes.
        """

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
    """
    User Output Schema.

    Defines the structure for the user information returned by the API.

    Attributes:
        id (PyObjectId): The unique identifier of the user.
        wallet (Optional[Wallet]): The wallet information associated with the user.
    """

    id: PyObjectId = Field(
        default_factory=PyObjectId, alias="_id", description="The unique identifier of the user."
    )
    wallet: Optional[Wallet] = Field(
        None, description="The wallet information associated with the user."
    )

    class Config:
        """
        Configuration for the UserOut Schema.

        Enables ORM mode, allows population by field name, and defines JSON encoders for ObjectId.
        Provides example data for documentation purposes.
        """

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
    """
    Paginated Users Output Schema.

    Defines the structure for a paginated list of users returned by the API.

    Attributes:
        users (List[UserOut]): A list of user objects.
        total (int): The total number of users.
        page (int): The current page number.
        limit (int): The number of users per page.
    """

    users: List[UserOut] = Field(
        ..., description="A list of user objects."
    )
    total: int = Field(
        ..., description="The total number of users."
    )
    page: int = Field(
        ..., description="The current page number."
    )
    limit: int = Field(
        ..., description="The number of users per page."
    )

    class Config:
        """
        Configuration for the UsersOut Schema.

        Provides example data for documentation purposes.
        """

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
    """
    User Deletion Confirmation Schema.

    Defines the structure for the confirmation message returned after deleting a user.

    Attributes:
        id (str): The unique identifier of the deleted user.
        username (str): The username of the deleted user.
        email (EmailStr): The email address of the deleted user.
        role (str): The role of the deleted user.
    """

    id: str = Field(
        ..., description="The unique identifier of the deleted user."
    )
    username: str = Field(
        ..., description="The username of the deleted user."
    )
    email: EmailStr = Field(
        ..., description="The email address of the deleted user."
    )
    role: str = Field(
        ..., description="The role of the deleted user."
    )

    class Config:
        """
        Configuration for the UserOutDelete Schema.

        Provides example data for documentation purposes.
        """

        schema_extra = {
            "example": {
                "id": "user_id",
                "username": "Mohamad",
                "email": "mab13401@mail.com",
                "role": "user"
            }
        }


class WalletTransaction(BaseModel):
    """
    Wallet Transaction Schema.

    Defines the structure for wallet transactions.

    Attributes:
        amount (float): The amount to be added or deducted from the wallet.
    """

    amount: float = Field(
        ..., description="The amount to be added or deducted from the wallet."
    )

    class Config:
        """
        Configuration for the WalletTransaction Schema.

        Provides example data for documentation purposes.
        """

        schema_extra = {
            "example": {
                "amount": 50.0
            }
        }

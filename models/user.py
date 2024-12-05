"""
User Models Module.

This module defines the `UserModel` class, representing user data within the application.
It utilizes Pydantic for data validation and integrates with MongoDB through the custom `PyObjectId`.
"""

from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from app.models.pyobjectid import PyObjectId


class UserModel(BaseModel):
    """
    User Model.

    Represents a user within the application, including authentication and role information.

    Attributes:
        id (PyObjectId): The unique identifier for the user, mapped from MongoDB's `_id`.
        username (str): The user's chosen username.
        email (EmailStr): The user's email address.
        hashed_password (str): The hashed password for authentication.
        role (str): The user's role within the application. Defaults to "user".
    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: EmailStr
    hashed_password: str
    role: str = "user"

    class Config:
        """
        Configuration for the `UserModel`.

        Allows arbitrary types and defines JSON encoders for `ObjectId`.
        """

        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

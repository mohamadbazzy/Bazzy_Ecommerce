"""
Authentication Schemas Module.

This module defines the Pydantic models related to user authentication, including
token generation, user signup, and user output representations. These schemas are used for
validating and serializing data in authentication-related API endpoints.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Token(BaseModel):
    """
    Token Schema.

    Defines the structure for the JWT token returned upon successful authentication.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of the token (e.g., "bearer").
    """

    access_token: str = Field(
        ..., description="The JWT access token."
    )
    token_type: str = Field(
        ..., description="The type of the token (e.g., 'bearer')."
    )


class Signup(BaseModel):
    """
    Signup Schema.

    Defines the structure for user signup requests.

    Attributes:
        username (str): The desired username of the user.
        email (EmailStr): The email address of the user.
        password (str): The plain-text password for the user.
        role (Optional[str]): The role of the user (e.g., "user", "admin"). Defaults to "user".
    """

    username: str = Field(
        ..., description="The desired username of the user."
    )
    email: EmailStr = Field(
        ..., description="The email address of the user."
    )
    password: str = Field(
        ..., description="The plain-text password for the user."
    )
    role: Optional[str] = Field(
        "user", description="The role of the user (e.g., 'user', 'admin')."
    )


class UserOut(BaseModel):
    """
    User Output Schema.

    Defines the structure for the user information returned by the API.

    Attributes:
        id (str): The unique identifier of the user.
        username (str): The username of the user.
        email (EmailStr): The email address of the user.
        role (str): The role of the user.
    """

    id: str = Field(
        ..., description="The unique identifier of the user."
    )
    username: str = Field(
        ..., description="The username of the user."
    )
    email: EmailStr = Field(
        ..., description="The email address of the user."
    )
    role: str = Field(
        ..., description="The role of the user."
    )


class UserInDB(UserOut):
    """
    User In Database Schema.

    Extends `UserOut` to include the hashed password for internal use.

    Attributes:
        hashed_password (str): The hashed password of the user.
    """

    hashed_password: str = Field(
        ..., description="The hashed password of the user."
    )

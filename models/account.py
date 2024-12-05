"""
Custom PyObjectId Type Module.

This module defines a custom `PyObjectId` class that extends MongoDB's `ObjectId` to be compatible with Pydantic models.
It includes validation methods to ensure the integrity of ObjectId fields.
"""

from bson import ObjectId
from pydantic import BaseModel


class PyObjectId(ObjectId):
    """
    Custom ObjectId type for Pydantic models.

    This class extends MongoDB's `ObjectId` to integrate seamlessly with Pydantic's validation system.

    Methods:
        __get_validators__: Yields the validator method for Pydantic.
        validate: Validates and converts input to `ObjectId`.
    """

    @classmethod
    def __get_validators__(cls):
        """
        Yield validator methods for Pydantic.

        Yields:
            Callable: The validator function.
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """
        Validate and convert the input to an `ObjectId`.

        Args:
            v (str | ObjectId): The value to validate.

        Returns:
            ObjectId: The validated `ObjectId`.

        Raises:
            ValueError: If the input is not a valid `ObjectId`.
        """
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
"""
Account Models Module.

This module defines the data models related to user accounts, including the `AccountModel`.
It utilizes Pydantic for data validation and MongoDB's `ObjectId` for unique identifiers.
"""

from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from app.models.pyobjectid import PyObjectId


class AccountModel(BaseModel):
    """
    User Account Model.

    Represents a user's account with related information.

    Attributes:
        id (PyObjectId): The unique identifier for the account, mapped from MongoDB's `_id`.
        user_id (PyObjectId): The identifier of the user owning the account.
        address (Optional[str]): The address associated with the account.
        phone_number (Optional[str]): The phone number associated with the account.
    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    address: Optional[str]
    phone_number: Optional[str]

    class Config:
        """
        Configuration for the `AccountModel`.

        Allows arbitrary types and defines JSON encoders for `ObjectId`.
        """
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

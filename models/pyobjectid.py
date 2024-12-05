"""
PyObjectId Module.

This module defines the `PyObjectId` class, a custom type that extends MongoDB's `ObjectId`.
It integrates seamlessly with Pydantic models, enabling the validation and serialization
of MongoDB ObjectIds within Pydantic schemas.
"""

from bson import ObjectId


class PyObjectId(ObjectId):
    """
    Custom ObjectId Type for Pydantic Models.

    Extends MongoDB's `ObjectId` to work with Pydantic's validation system.
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

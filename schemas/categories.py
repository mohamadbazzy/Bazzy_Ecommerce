"""
Categories Schemas Module.

This module defines the Pydantic models related to product category operations, including
category creation, updating, deletion, and output representations. These schemas are used for
validating and serializing data in category-related API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class CategoryCreate(BaseModel):
    """
    Category Creation Schema.

    Defines the structure for creating a new product category.

    Attributes:
        name (str): The name of the category.
        description (Optional[str]): A brief description of the category.
    """

    name: str = Field(
        ..., description="The name of the category."
    )
    description: Optional[str] = Field(
        None, description="A brief description of the category."
    )


class CategoryUpdate(BaseModel):
    """
    Category Update Schema.

    Defines the structure for updating an existing product category.

    Attributes:
        name (Optional[str]): The new name of the category.
        description (Optional[str]): The new description of the category.
    """

    name: Optional[str] = Field(
        None, description="The new name of the category."
    )
    description: Optional[str] = Field(
        None, description="The new description of the category."
    )


class CategoryOut(BaseModel):
    """
    Category Output Schema.

    Defines the structure for the category information returned by the API.

    Attributes:
        id (str): The unique identifier of the category.
        name (str): The name of the category.
        description (Optional[str]): A brief description of the category.
    """

    id: str = Field(
        ..., description="The unique identifier of the category."
    )
    name: str = Field(
        ..., description="The name of the category."
    )
    description: Optional[str] = Field(
        None, description="A brief description of the category."
    )


class CategoryOutDelete(BaseModel):
    """
    Category Deletion Confirmation Schema.

    Defines the structure for the confirmation message returned after deleting a category.

    Attributes:
        id (str): The unique identifier of the deleted category.
        status (str): The status message indicating successful deletion.
    """

    id: str = Field(
        ..., description="The unique identifier of the deleted category."
    )
    status: str = Field(
        ..., description="The status message indicating successful deletion."
    )


class CategoriesOut(BaseModel):
    """
    Paginated Categories Output Schema.

    Defines the structure for a paginated list of categories returned by the API.

    Attributes:
        categories (List[CategoryOut]): A list of category objects.
        page (int): The current page number.
        limit (int): The number of items per page.
    """

    categories: List[CategoryOut] = Field(
        ..., description="A list of category objects."
    )
    page: int = Field(
        ..., description="The current page number."
    )
    limit: int = Field(
        ..., description="The number of items per page."
    )

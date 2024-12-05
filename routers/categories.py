"""
Categories Router Module.

This module defines the API endpoints related to product category management, including
retrieving all categories, fetching a specific category, creating a new category, updating
an existing category, and deleting a category. Administrative privileges are required for
creating, updating, and deleting categories.
"""

from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.categories import CategoryService
from sqlalchemy.orm import Session
from app.schemas.categories import CategoryCreate, CategoryOut, CategoriesOut, CategoryOutDelete, CategoryUpdate
from app.core.security import check_admin_role
from typing import Optional

router = APIRouter(tags=["Categories"], prefix="/categories")

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CategoriesOut)
def get_all_categories(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query("", description="Search based name of categories"),
):
    """
    Retrieve All Categories.

    Fetches a paginated list of all product categories, optionally filtering by name.

    Args:
        db (Session): The SQLAlchemy database session.
        page (int): The page number for pagination.
        limit (int): The number of items per page.
        search (Optional[str]): The search query to filter categories by name.

    Returns:
        CategoriesOut: A paginated list of product categories.
    """
    return CategoryService.get_all_categories(db, page, limit, search)

@router.get(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a Specific Category by ID.

    Fetches the details of a single product category identified by its ID.

    Args:
        category_id (int): The unique identifier of the category.
        db (Session): The SQLAlchemy database session.

    Returns:
        CategoryOut: The details of the requested product category.
    """
    return CategoryService.get_category(db, category_id)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryOut,
    dependencies=[Depends(check_admin_role)])
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a New Category.

    Creates a new product category with the provided category data. Requires administrative privileges.

    Args:
        category (CategoryCreate): The data for the new category.
        db (Session): The SQLAlchemy database session.

    Returns:
        CategoryOut: The details of the created product category.
    """
    return CategoryService.create_category(db, category)

@router.put(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryOut,
    dependencies=[Depends(check_admin_role)])
def update_category(category_id: int, updated_category: CategoryUpdate, db: Session = Depends(get_db)):
    """
    Update an Existing Category.

    Updates the details of an existing product category identified by its ID. Requires administrative privileges.

    Args:
        category_id (int): The unique identifier of the category to be updated.
        updated_category (CategoryUpdate): The updated category data.
        db (Session): The SQLAlchemy database session.

    Returns:
        CategoryOut: The details of the updated product category.
    """
    return CategoryService.update_category(db, category_id, updated_category)

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryOutDelete,
    dependencies=[Depends(check_admin_role)])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a Category by ID.

    Permanently removes a product category identified by its ID from the system. Requires administrative privileges.

    Args:
        category_id (int): The unique identifier of the category to be deleted.
        db (Session): The SQLAlchemy database session.

    Returns:
        CategoryOutDelete: Confirmation details of the deleted product category.
    """
    return CategoryService.delete_category(db, category_id)

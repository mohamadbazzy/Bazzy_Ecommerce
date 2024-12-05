"""
Categories Service Module.

This module defines the `CategoryService` class, which manages product category
operations such as retrieving all categories, fetching a specific category, creating
a new category, updating an existing category, and deleting a category. It interacts
with the database to perform CRUD operations on category data.
"""

from app.db.database import database
from app.schemas.categories import CategoryCreate, CategoryUpdate
from bson import ObjectId
from fastapi import HTTPException


class CategoryService:
    """
    Service class for managing product categories.
    """

    @staticmethod
    async def get_all_categories(db, page, limit, search):
        """
        Retrieve all product categories with pagination and optional search.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            page (int): The current page number.
            limit (int): The number of categories per page.
            search (str): The search query to filter categories by name.

        Returns:
            dict: A dictionary containing a list of categories, current page, and limit.
        """
        skip = (page - 1) * limit
        query = {}
        if search:
            query["name"] = {"$regex": search, "$options": "i"}
        categories_cursor = database["categories"].find(query).skip(skip).limit(limit)
        categories = await categories_cursor.to_list(length=limit)
        for category in categories:
            category["id"] = str(category["_id"])
        return {"categories": categories, "page": page, "limit": limit}

    @staticmethod
    async def get_category(db, category_id):
        """
        Retrieve a specific product category by its ID.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            category_id (str): The unique identifier of the category.

        Returns:
            dict: A dictionary containing the category details.

        Raises:
            HTTPException: If the category is not found.
        """
        category = await database["categories"].find_one({"_id": ObjectId(category_id)})
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        category["id"] = str(category["_id"])
        return category

    @staticmethod
    async def create_category(db, category_data: CategoryCreate):
        """
        Create a new product category.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            category_data (CategoryCreate): The category data to be created.

        Returns:
            dict: A dictionary containing the created category details.
        """
        category_dict = category_data.dict()
        result = await database["categories"].insert_one(category_dict)
        category_dict["_id"] = result.inserted_id
        category_dict["id"] = str(category_dict["_id"])
        return category_dict

    @staticmethod
    async def update_category(db, category_id, updated_category: CategoryUpdate):
        """
        Update an existing product category.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            category_id (str): The unique identifier of the category to be updated.
            updated_category (CategoryUpdate): The updated category data.

        Returns:
            dict: A dictionary containing the updated category details.

        Raises:
            HTTPException: If the category is not found or not modified.
        """
        update_data = updated_category.dict(exclude_unset=True)
        result = await database["categories"].update_one(
            {"_id": ObjectId(category_id)},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Category not found or not modified")
        return await CategoryService.get_category(db, category_id)

    @staticmethod
    async def delete_category(db, category_id):
        """
        Delete a product category by its ID.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            category_id (str): The unique identifier of the category to be deleted.

        Returns:
            dict: A confirmation dictionary indicating successful deletion.

        Raises:
            HTTPException: If the category is not found.
        """
        result = await database["categories"].delete_one({"_id": ObjectId(category_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Category not found")
        return {"id": category_id, "status": "deleted"}

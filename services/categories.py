from app.db.database import database
from app.schemas.categories import CategoryCreate, CategoryUpdate
from bson import ObjectId
from fastapi import HTTPException

class CategoryService:

    @staticmethod
    async def get_all_categories(db, page, limit, search):
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
        category = await database["categories"].find_one({"_id": ObjectId(category_id)})
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        category["id"] = str(category["_id"])
        return category

    @staticmethod
    async def create_category(db, category_data: CategoryCreate):
        category_dict = category_data.dict()
        result = await database["categories"].insert_one(category_dict)
        category_dict["_id"] = result.inserted_id
        category_dict["id"] = str(category_dict["_id"])
        return category_dict

    @staticmethod
    async def update_category(db, category_id, updated_category: CategoryUpdate):
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
        result = await database["categories"].delete_one({"_id": ObjectId(category_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Category not found")
        return {"id": category_id, "status": "deleted"}

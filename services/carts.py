"""
Carts Service Module.

This module defines the `CartService` class, which manages shopping cart operations
such as retrieving all carts, fetching a specific cart, creating a new cart, updating
an existing cart, and deleting a cart. It enforces authorization based on user roles
and interacts with the database to perform CRUD operations on cart data.
"""

from app.db.database import database
from app.core.security import get_current_user
from app.schemas.carts import CartCreate, CartUpdate
from bson import ObjectId
from fastapi import HTTPException


class CartService:
    """
    Service class for managing shopping carts.
    """

    @staticmethod
    async def get_all_carts(token, db, page, limit):
        """
        Retrieve all shopping carts with pagination.

        Args:
            token: The JWT token containing user credentials.
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            page (int): The current page number.
            limit (int): The number of carts per page.

        Returns:
            dict: A dictionary containing a list of carts, current page, and limit.

        Raises:
            HTTPException: If the user is not authorized.
        """
        user = await get_current_user(token)
        if user["role"] != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        skip = (page - 1) * limit
        carts_cursor = database["carts"].find().skip(skip).limit(limit)
        carts = await carts_cursor.to_list(length=limit)
        for cart in carts:
            cart["id"] = str(cart["_id"])
            cart["user_id"] = str(cart["user_id"])
        return {"carts": carts, "page": page, "limit": limit}

    @staticmethod
    async def get_cart(token, db, cart_id):
        """
        Retrieve a specific shopping cart by its ID.

        Args:
            token: The JWT token containing user credentials.
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            cart_id (str): The unique identifier of the cart.

        Returns:
            dict: A dictionary containing the cart details.

        Raises:
            HTTPException: If the cart is not found or the user is not authorized.
        """
        user = await get_current_user(token)
        cart = await database["carts"].find_one({"_id": ObjectId(cart_id)})
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        if cart["user_id"] != user["_id"] and user["role"] != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        cart["id"] = str(cart["_id"])
        cart["user_id"] = str(cart["user_id"])
        return cart

    @staticmethod
    async def create_cart(token, db, cart_data: CartCreate):
        """
        Create a new shopping cart for the authenticated user.

        Args:
            token: The JWT token containing user credentials.
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            cart_data (CartCreate): The cart data to be created.

        Returns:
            dict: A dictionary containing the created cart details.

        Raises:
            HTTPException: If the cart creation fails.
        """
        user = await get_current_user(token)
        cart_dict = {
            "user_id": ObjectId(user["_id"]),
            "items": cart_data.items
        }
        result = await database["carts"].insert_one(cart_dict)
        cart_dict["_id"] = result.inserted_id
        cart_dict["id"] = str(cart_dict["_id"])
        cart_dict["user_id"] = str(cart_dict["user_id"])
        return cart_dict

    @staticmethod
    async def update_cart(token, db, cart_id, updated_cart: CartUpdate):
        """
        Update an existing shopping cart.

        Args:
            token: The JWT token containing user credentials.
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            cart_id (str): The unique identifier of the cart to be updated.
            updated_cart (CartUpdate): The updated cart data.

        Returns:
            dict: A dictionary containing the updated cart details.

        Raises:
            HTTPException: If the cart is not found, the user is not authorized, or the cart is not modified.
        """
        user = await get_current_user(token)
        cart = await database["carts"].find_one({"_id": ObjectId(cart_id)})
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        if cart["user_id"] != user["_id"]:
            raise HTTPException(status_code=403, detail="Not authorized")
        update_data = updated_cart.dict(exclude_unset=True)
        result = await database["carts"].update_one(
            {"_id": ObjectId(cart_id)},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=304, detail="Cart not modified")
        return await CartService.get_cart(token, db, cart_id)

    @staticmethod
    async def delete_cart(token, db, cart_id):
        """
        Delete a shopping cart by its ID.

        Args:
            token: The JWT token containing user credentials.
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            cart_id (str): The unique identifier of the cart to be deleted.

        Returns:
            dict: A confirmation dictionary indicating successful deletion.

        Raises:
            HTTPException: If the cart is not found or the user is not authorized.
        """
        user = await get_current_user(token)
        cart = await database["carts"].find_one({"_id": ObjectId(cart_id)})
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        if cart["user_id"] != user["_id"]:
            raise HTTPException(status_code=403, detail="Not authorized")
        result = await database["carts"].delete_one({"_id": ObjectId(cart_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Cart not found")
        return {"id": cart_id, "status": "deleted"}

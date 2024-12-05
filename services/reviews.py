"""
Reviews Service Module.

This module defines the `ReviewsService` class, which manages product review
operations such as submitting, updating, deleting reviews, retrieving reviews for
specific products or customers, and moderating reviews. It interacts with the
database to perform CRUD operations on review data.
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.schemas.reviews import SubmitReviewRequest, UpdateReviewRequest, ModerateReviewRequest, ReviewDetails


class ReviewsService:
    """
    Service class for managing product reviews.
    """

    @staticmethod
    async def submit_review(db: AsyncIOMotorDatabase, review: SubmitReviewRequest):
        """
        Submit a new review for a product.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            review (SubmitReviewRequest): The review data to be submitted.

        Returns:
            dict: A dictionary containing a success message and the review ID.

        Raises:
            HTTPException: If the product or user is not found.
        """
        product = await db["products"].find_one({"_id": review.product_id})
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        user = await db["users"].find_one({"username": review.username})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        new_review = {
            "product_id": review.product_id,
            "username": review.username,
            "rating": review.rating,
            "comment": review.comment,
            "status": "pending",  # Default status for moderation
        }
        result = await db["reviews"].insert_one(new_review)
        return {"message": "Review submitted successfully", "id": str(result.inserted_id)}

    @staticmethod
    async def update_review(db: AsyncIOMotorDatabase, review_id: str, review: UpdateReviewRequest):
        """
        Update an existing review.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            review_id (str): The unique identifier of the review to be updated.
            review (UpdateReviewRequest): The updated review data.

        Returns:
            dict: A dictionary containing a success message.

        Raises:
            HTTPException: If the review is not found.
        """
        result = await db["reviews"].update_one(
            {"_id": review_id},
            {"$set": {"rating": review.rating, "comment": review.comment}},
        )
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
            )
        return {"message": "Review updated successfully"}

    @staticmethod
    async def delete_review(db: AsyncIOMotorDatabase, review_id: str):
        """
        Delete a review by its ID.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            review_id (str): The unique identifier of the review to be deleted.

        Returns:
            dict: A dictionary containing a success message.

        Raises:
            HTTPException: If the review is not found.
        """
        result = await db["reviews"].delete_one({"_id": review_id})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
            )
        return {"message": "Review deleted successfully"}

    @staticmethod
    async def get_product_reviews(db: AsyncIOMotorDatabase, product_id: str):
        """
        Retrieve all reviews for a specific product.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            product_id (str): The unique identifier of the product.

        Returns:
            list: A list of review dictionaries.
        """
        reviews = await db["reviews"].find({"product_id": product_id}).to_list(length=100)
        return reviews

    @staticmethod
    async def get_customer_reviews(db: AsyncIOMotorDatabase, username: str):
        """
        Retrieve all reviews submitted by a specific customer.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            username (str): The username of the customer.

        Returns:
            list: A list of review dictionaries.
        """
        reviews = await db["reviews"].find({"username": username}).to_list(length=100)
        return reviews

    @staticmethod
    async def moderate_review(db: AsyncIOMotorDatabase, review_id: str, moderation_request: ModerateReviewRequest):
        """
        Moderate a review by updating its status.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            review_id (str): The unique identifier of the review to be moderated.
            moderation_request (ModerateReviewRequest): The moderation actions to be applied.

        Returns:
            dict: A dictionary containing a success message.

        Raises:
            HTTPException: If the review is not found.
        """
        result = await db["reviews"].update_one(
            {"_id": review_id}, {"$set": {"status": moderation_request.status}}
        )
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
            )
        return {"message": "Review status updated successfully"}

    @staticmethod
    async def get_review_details(db: AsyncIOMotorDatabase, review_id: str):
        """
        Retrieve detailed information of a specific review.

        Args:
            db (AsyncIOMotorDatabase): The MongoDB database instance.
            review_id (str): The unique identifier of the review.

        Returns:
            dict: A dictionary containing the review details.

        Raises:
            HTTPException: If the review is not found.
        """
        review = await db["reviews"].find_one({"_id": review_id})
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
            )
        return review

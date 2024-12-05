from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.schemas.reviews import SubmitReviewRequest, UpdateReviewRequest, ModerateReviewRequest

class ReviewsService:
    @staticmethod
    async def submit_review(db: AsyncIOMotorDatabase, review: SubmitReviewRequest):
        """Submit a review for a product"""
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
        """Update an existing review"""
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
        """Delete a review"""
        result = await db["reviews"].delete_one({"_id": review_id})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
            )
        return {"message": "Review deleted successfully"}

    @staticmethod
    async def get_product_reviews(db: AsyncIOMotorDatabase, product_id: str):
        """Get all reviews for a specific product"""
        reviews = await db["reviews"].find({"product_id": product_id}).to_list(length=100)
        return reviews

    @staticmethod
    async def get_customer_reviews(db: AsyncIOMotorDatabase, username: str):
        """Get all reviews submitted by a specific customer"""
        reviews = await db["reviews"].find({"username": username}).to_list(length=100)
        return reviews

    @staticmethod
    async def moderate_review(db: AsyncIOMotorDatabase, review_id: str, moderation_request: ModerateReviewRequest):
        """Moderate a review"""
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
        """Get details of a specific review"""
        review = await db["reviews"].find_one({"_id": review_id})
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
            )
        return review

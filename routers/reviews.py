"""
Reviews Router Module.

This module defines the API endpoints related to product reviews, including submitting,
updating, deleting reviews, retrieving reviews for specific products or customers, and
moderating reviews. It utilizes dependency injection for database access and user authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.reviews import (
    SubmitReviewRequest,
    UpdateReviewRequest,
    ReviewResponse,
    ModerateReviewRequest,
    ReviewDetails,
)
from app.services.reviews import ReviewsService
from app.db.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.post("/reviews", status_code=201)
async def submit_review(review: SubmitReviewRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Submit a Review for a Product.

    Allows a user to submit a review for a specific product.

    Args:
        review (SubmitReviewRequest): The review data submitted by the user.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        ReviewResponse: The submitted review details.
    """
    return await ReviewsService.submit_review(db, review)

@router.put("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: str, review: UpdateReviewRequest, db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Update an Existing Review.

    Allows a user to update their existing review identified by its ID.

    Args:
        review_id (str): The unique identifier of the review to be updated.
        review (UpdateReviewRequest): The updated review data.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        ReviewResponse: The updated review details.
    """
    return await ReviewsService.update_review(db, review_id, review)

@router.delete("/reviews/{review_id}", status_code=204)
async def delete_review(review_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Delete a Review.

    Permanently removes a review identified by its ID from the system.

    Args:
        review_id (str): The unique identifier of the review to be deleted.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        None: Returns a 204 No Content status upon successful deletion.
    """
    return await ReviewsService.delete_review(db, review_id)

@router.get("/reviews/products/{product_id}", response_model=List[ReviewResponse])
async def get_product_reviews(product_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get All Reviews for a Specific Product.

    Retrieves all reviews associated with a particular product.

    Args:
        product_id (str): The unique identifier of the product.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        List[ReviewResponse]: A list of reviews for the specified product.
    """
    return await ReviewsService.get_product_reviews(db, product_id)

@router.get("/reviews/customers/{username}", response_model=List[ReviewResponse])
async def get_customer_reviews(username: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get All Reviews Submitted by a Specific Customer.

    Retrieves all reviews submitted by a particular customer identified by their username.

    Args:
        username (str): The username of the customer.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        List[ReviewResponse]: A list of reviews submitted by the specified customer.
    """
    return await ReviewsService.get_customer_reviews(db, username)

@router.put("/reviews/moderate/{review_id}", response_model=ReviewResponse)
async def moderate_review(
    review_id: str, moderation_request: ModerateReviewRequest, db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Moderate a Review.

    Allows an administrator to moderate a review, such as approving or rejecting it.

    Args:
        review_id (str): The unique identifier of the review to be moderated.
        moderation_request (ModerateReviewRequest): The moderation actions to be applied.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        ReviewResponse: The moderated review details.
    """
    return await ReviewsService.moderate_review(db, review_id, moderation_request)

@router.get("/reviews/{review_id}", response_model=ReviewDetails)
async def get_review_details(review_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get Details of a Specific Review.

    Retrieves detailed information about a specific review identified by its ID.

    Args:
        review_id (str): The unique identifier of the review.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        ReviewDetails: The detailed information of the specified review.
    """
    return await ReviewsService.get_review_details(db, review_id)

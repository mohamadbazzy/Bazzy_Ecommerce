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
    """Submit a review for a product"""
    return await ReviewsService.submit_review(db, review)

@router.put("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: str, review: UpdateReviewRequest, db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update an existing review"""
    return await ReviewsService.update_review(db, review_id, review)

@router.delete("/reviews/{review_id}", status_code=204)
async def delete_review(review_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Delete a review"""
    return await ReviewsService.delete_review(db, review_id)

@router.get("/reviews/products/{product_id}", response_model=List[ReviewResponse])
async def get_product_reviews(product_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get all reviews for a specific product"""
    return await ReviewsService.get_product_reviews(db, product_id)

@router.get("/reviews/customers/{username}", response_model=List[ReviewResponse])
async def get_customer_reviews(username: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get all reviews submitted by a specific customer"""
    return await ReviewsService.get_customer_reviews(db, username)

@router.put("/reviews/moderate/{review_id}", response_model=ReviewResponse)
async def moderate_review(
    review_id: str, moderation_request: ModerateReviewRequest, db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Moderate a review"""
    return await ReviewsService.moderate_review(db, review_id, moderation_request)

@router.get("/reviews/{review_id}", response_model=ReviewDetails)
async def get_review_details(review_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get details of a specific review"""
    return await ReviewsService.get_review_details(db, review_id)

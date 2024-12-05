from pydantic import BaseModel, Field
from typing import Optional


class SubmitReviewRequest(BaseModel):
    product_id: str
    username: str
    rating: int = Field(..., ge=1, le=5)
    comment: str


class UpdateReviewRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str


class ReviewResponse(BaseModel):
    id: str
    product_id: str
    username: str
    rating: int
    comment: str
    status: str


class ModerateReviewRequest(BaseModel):
    status: str


class ReviewDetails(ReviewResponse):
    pass

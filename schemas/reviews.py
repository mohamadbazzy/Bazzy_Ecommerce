"""
Reviews Schemas Module.

This module defines the Pydantic models related to product review operations, including
submitting, updating, moderating, and retrieving reviews. These schemas are used for
validating and serializing data in review-related API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class SubmitReviewRequest(BaseModel):
    """
    Submit Review Request Schema.

    Defines the structure for submitting a new review for a product.

    Attributes:
        product_id (str): The unique identifier of the product being reviewed.
        username (str): The username of the reviewer.
        rating (int): The rating given to the product (1 to 5).
        comment (str): The review comment.
    """

    product_id: str = Field(
        ..., description="The unique identifier of the product being reviewed."
    )
    username: str = Field(
        ..., description="The username of the reviewer."
    )
    rating: int = Field(
        ..., ge=1, le=5, description="The rating given to the product (1 to 5)."
    )
    comment: str = Field(
        ..., description="The review comment."
    )


class UpdateReviewRequest(BaseModel):
    """
    Update Review Request Schema.

    Defines the structure for updating an existing review.

    Attributes:
        rating (int): The new rating for the product (1 to 5).
        comment (str): The new review comment.
    """

    rating: int = Field(
        ..., ge=1, le=5, description="The new rating for the product (1 to 5)."
    )
    comment: str = Field(
        ..., description="The new review comment."
    )


class ReviewResponse(BaseModel):
    """
    Review Response Schema.

    Defines the structure for the review information returned by the API.

    Attributes:
        id (str): The unique identifier of the review.
        product_id (str): The unique identifier of the product being reviewed.
        username (str): The username of the reviewer.
        rating (int): The rating given to the product.
        comment (str): The review comment.
        status (str): The status of the review (e.g., "approved", "pending", "rejected").
    """

    id: str = Field(
        ..., description="The unique identifier of the review."
    )
    product_id: str = Field(
        ..., description="The unique identifier of the product being reviewed."
    )
    username: str = Field(
        ..., description="The username of the reviewer."
    )
    rating: int = Field(
        ..., description="The rating given to the product."
    )
    comment: str = Field(
        ..., description="The review comment."
    )
    status: str = Field(
        ..., description="The status of the review (e.g., 'approved', 'pending', 'rejected')."
    )


class ModerateReviewRequest(BaseModel):
    """
    Moderate Review Request Schema.

    Defines the structure for moderating a review.

    Attributes:
        status (str): The new status of the review (e.g., "approved", "rejected").
    """

    status: str = Field(
        ..., description="The new status of the review (e.g., 'approved', 'rejected')."
    )


class ReviewDetails(ReviewResponse):
    """
    Review Details Schema.

    Extends `ReviewResponse` to include additional detailed information about a review.
    """
    pass

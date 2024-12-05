"""
Sales Router Module.

This module defines the API endpoints related to sales operations, including displaying available goods,
retrieving details of specific goods, processing sales transactions, and adding new goods to the database.
It utilizes dependency injection for database access and ensures that only authorized users can perform certain actions.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.sales import Good, GoodDetails, SaleRequest, SaleResponse, AddGoodRequest
from app.services.sales import SalesService
from app.db.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.get("/goods", response_model=List[Good])
async def get_goods(db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Display Available Goods.

    Retrieves a list of all goods currently available in the system.

    Args:
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        List[Good]: A list of available goods.
    """
    return await SalesService.get_goods(db)

@router.get("/goods/{good_name}", response_model=GoodDetails)
async def get_good_details(good_name: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get Details of a Specific Good.

    Retrieves detailed information about a specific good identified by its name.

    Args:
        good_name (str): The name of the good.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        GoodDetails: The detailed information of the specified good.
    """
    return await SalesService.get_good_details(db, good_name)

@router.post("/sales", response_model=SaleResponse)
async def make_sale(sale_request: SaleRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Process a Sale.

    Processes a sales transaction based on the provided sale request data.

    Args:
        sale_request (SaleRequest): The details of the sale to be processed.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        SaleResponse: The details of the processed sale.
    """
    return await SalesService.process_sale(db, sale_request)

@router.post("/goods", status_code=201)
async def add_good(good: AddGoodRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Add a New Good to the Database.

    Adds a new good to the database with the provided good data.

    Args:
        good (AddGoodRequest): The data for the new good.
        db (AsyncIOMotorDatabase): The MongoDB database instance.

    Returns:
        dict: A confirmation message indicating successful addition.
    """
    await SalesService.add_good(db, good)
    return {"message": "Good added successfully"}

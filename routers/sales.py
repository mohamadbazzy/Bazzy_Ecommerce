from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.sales import Good, GoodDetails, SaleRequest, SaleResponse
from app.services.sales import SalesService
from app.db.database import get_databas
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.get("/goods", response_model=List[Good])
async def get_goods(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Display available goods"""
    return await SalesService.get_goods(db)


@router.get("/goods/{good_name}", response_model=GoodDetails)
async def get_good_details(good_name: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get details of a specific good"""
    return await SalesService.get_good_details(db, good_name)


@router.post("/sales", response_model=SaleResponse)
async def make_sale(sale_request: SaleRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Process a sale"""
    return await SalesService.process_sale(db, sale_request)
c
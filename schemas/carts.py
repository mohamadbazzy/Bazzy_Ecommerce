from pydantic import BaseModel
from typing import List

class CartItem(BaseModel):
    product_id: str
    quantity: int

class CartCreate(BaseModel):
    items: List[CartItem]

class CartUpdate(BaseModel):
    items: List[CartItem]

class CartOut(BaseModel):
    id: str
    user_id: str
    items: List[CartItem]

class CartOutDelete(BaseModel):
    id: str
    status: str

class CartsOut(BaseModel):
    carts: List[CartOut]
    page: int
    limit: int

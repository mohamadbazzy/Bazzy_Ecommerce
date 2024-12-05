from pydantic import BaseModel
from typing import Optional, List

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str]

class CategoryUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

class CategoryOut(BaseModel):
    id: str
    name: str
    description: Optional[str]

class CategoryOutDelete(BaseModel):
    id: str
    status: str

class CategoriesOut(BaseModel):
    categories: List[CategoryOut]
    page: int
    limit: int

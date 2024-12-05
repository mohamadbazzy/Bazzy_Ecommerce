from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from app.models.pyobjectid import PyObjectId

class CategoryModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

from typing import List, Optional

from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Pizza")
    price: float = Field(..., gt=0, example=9.99)
    stock: int = Field(..., ge=0, example=10)
    description: str = Field(..., example="Delicious cheese pizza")
    category: str = Field(..., example="Food")
    is_available: bool = Field(default=True, example=True)
    tags: Optional[List[str]] = Field(default=None, example=["cheese", "vegetarian"])


products: List[Product] = []

from typing import Optional

from pydantic import BaseModel, Field


class MenuItem(BaseModel):
    id: int = Field(default=None, example=1)
    name: str = Field(..., example="Margherita")
    description: str = Field(..., example="Classic cheese and tomato pizza")
    price: float = Field(..., gt=0, example=9.99)
    category: str = Field(..., example="Pizza")
    is_vegetarian: bool = Field(default=False, example=True)
    calories: Optional[int] = Field(default=None, example=250)
    is_gluten_free: bool = Field(default=False, example=False)
    is_spicy: bool = Field(default=False, example=False)
    is_available: bool = Field(default=True, example=True)


menu_items: list[MenuItem] = []

from typing import List, Optional

from pydantic import BaseModel, Field


class Order(BaseModel):
    id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    product_ids: List[int] = Field(..., example=[1, 2])
    total_price: float = Field(..., gt=0, example=19.98)
    status: str = Field(..., example="Pending")
    delivery_address: str = Field(..., example="123 Pizza Street")
    order_date: str = Field(..., example="2023-10-01")
    delivery_date: Optional[str] = Field(default=None, example="2023-10-02")
    rewards_points_used: int = Field(default=0, ge=0, example=10)


orders: list[Order] = []

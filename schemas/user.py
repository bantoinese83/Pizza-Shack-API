from typing import List, Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(..., example="John Doe")
    email: str = Field(..., example="john.doe@example.com")
    phone: Optional[str] = Field(default=None, example="123-456-7890")
    address: Optional[str] = Field(default=None, example="123 Main St")
    is_active: bool = Field(default=True, example=True)
    created_at: str = Field(..., example="2023-10-01")
    rewards_points: int = Field(..., ge=0, example=100)


users: List[User] = []

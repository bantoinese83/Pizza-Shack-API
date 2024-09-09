# models/menu.py
from sqlalchemy import Column, Integer, String, Float, Boolean

from core.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category = Column(String)
    is_vegetarian = Column(Boolean, default=False)
    calories = Column(Integer, nullable=True)
    is_gluten_free = Column(Boolean, default=False)
    is_spicy = Column(Boolean, default=False)
    is_available = Column(Boolean, default=True)

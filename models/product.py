from sqlalchemy import Column, Integer, String, Float, Boolean

from core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    stock = Column(Integer)
    description = Column(String)
    category = Column(String)
    is_available = Column(Boolean, default=True)
    tags = Column(String, nullable=True)  # Store tags as a comma-separated string

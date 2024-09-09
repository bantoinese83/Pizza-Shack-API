# models/user.py
from sqlalchemy import Column, Integer, String, Boolean

from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True, nullable=True)
    address = Column(String, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(String)
    rewards_points = Column(Integer, default=0)

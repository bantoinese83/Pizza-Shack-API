# models/order.py
import json

from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_ids = Column(String)  # Store as comma-separated string
    total_price = Column(Float)
    status = Column(String)
    delivery_address = Column(String)
    order_date = Column(String)
    delivery_date = Column(String, nullable=True)
    rewards_points_used = Column(Integer, default=0)

    user = relationship("User")

    def set_product_ids(self, product_ids_list):
        self.product_ids = json.dumps(product_ids_list)

    def get_product_ids(self):
        return json.loads(self.product_ids)

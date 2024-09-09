# models/order.py
import json

from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base
from core.log_config import log


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_ids = Column(String, nullable=False)
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
        try:
            return json.loads(self.product_ids)
        except json.JSONDecodeError as e:
            log("ERROR", f"Error decoding product_ids for order {self.id}: {e}")
            return []

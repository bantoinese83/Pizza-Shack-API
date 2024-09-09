from sqlalchemy.orm import Session

from core.log_config import log_decorator
from core.middleware_config import logger
from models.order import Order
from schemas.order import Order as OrderSchema


@log_decorator("INFO")
def get_orders(db: Session):
    db_orders = db.query(Order).all()
    for db_order in db_orders:
        try:
            # Convert product_ids string back to a list
            db_order.product_ids = list(map(int, db_order.product_ids.split(',')))
        except ValueError as e:
            # Log the error and handle the invalid data
            logger.error(f"Error converting product_ids for order {db_order.id}: {e}")
            db_order.product_ids = []  # or handle it in another appropriate way
    return db_orders


def get_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order and isinstance(db_order.product_ids, str):
        # Convert product_ids string back to a list
        db_order.product_ids = list(map(int, db_order.product_ids.split(',')))
    return db_order


def create_order(db: Session, order: OrderSchema):
    # Convert product_ids list to a comma-separated string
    order_data = order.dict()
    order_data['product_ids'] = ','.join(map(str, order_data['product_ids']))
    order_data.pop('id', None)  # Ensure 'id' is not set manually

    db_order = Order(**order_data)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    # Convert product_ids string back to a list before returning
    db_order.product_ids = list(map(int, db_order.product_ids.split(',')))
    return db_order


def update_order(db: Session, order_id: int, order: OrderSchema):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        order_data = order.dict()
        # Convert product_ids list to a comma-separated string
        order_data['product_ids'] = ','.join(map(str, order_data['product_ids']))
        for key, value in order_data.items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
        # Convert product_ids string back to a list before returning
        db_order.product_ids = list(map(int, db_order.product_ids.split(',')))
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order

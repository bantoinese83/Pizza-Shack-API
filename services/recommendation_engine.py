from collections import Counter

from sqlalchemy.orm import Session

from core.log_config import log
from models.order import Order
from models.product import Product


def get_product_frequencies(orders):
    product_counter = Counter()
    for order in orders:
        try:
            product_ids = order.get_product_ids()
            product_counter.update(product_ids)
        except Exception as e:
            log("ERROR", f"Error processing order {order.id}: {e}")
    return product_counter


def get_user_preferences(db: Session, user_id: int):
    try:
        user_orders = db.query(Order).filter(Order.user_id == user_id).all()
        user_product_ids = [order.get_product_ids() for order in user_orders]
        user_product_counter = Counter([item for sublist in user_product_ids for item in sublist])
        return user_product_counter
    except Exception as e:
        log("ERROR", f"Error fetching user preferences for user_id {user_id}: {e}")
        return Counter()


def get_related_products(db: Session, product_id: int):
    try:
        # Example collaborative filtering logic
        related_products = Counter()
        orders_with_product = db.query(Order).filter(Order.product_ids.contains(str(product_id))).all()
        for order in orders_with_product:
            product_ids = order.get_product_ids()
            related_products.update(product_ids)
        related_products.pop(product_id, None)  # Remove the product itself from the recommendations
        return related_products
    except Exception as e:
        log("ERROR", f"Error fetching related products for product_id {product_id}: {e}")
        return Counter()


def get_category_products(db: Session, category: str):
    try:
        category_products = Counter()
        products = db.query(Product).filter(Product.category == category).all()
        for product in products:
            category_products[product.id] += 1
        return category_products
    except Exception as e:
        log("ERROR", f"Error fetching category products for category {category}: {e}")
        return Counter()

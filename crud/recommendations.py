from sqlalchemy.orm import Session

from core.log_config import log
from crud.order import get_past_orders
from services.recommendation_engine import get_product_frequencies, get_user_preferences, get_related_products, \
    get_category_products


def recommend_products(db: Session, top_n: int = 5, user_id: int = None, product_id: int = None, category: str = None):
    orders = get_past_orders(db)
    product_frequencies = get_product_frequencies(orders)
    log("INFO", f"Initial product frequencies: {product_frequencies}")

    if user_id:
        user_preferences = get_user_preferences(db, user_id)
        log("INFO", f"User preferences for user_id {user_id}: {user_preferences}")
        product_frequencies.update(user_preferences)

    if product_id:
        product_related = get_related_products(db, product_id)
        log("INFO", f"Related products for product_id {product_id}: {product_related}")
        product_frequencies.update(product_related)

    if category:
        category_products = get_category_products(db, category)
        log("INFO", f"Category products for category {category}: {category_products}")
        product_frequencies.update(category_products)

    log("INFO", f"Final product frequencies: {product_frequencies}")
    most_common_products = product_frequencies.most_common(top_n)
    return [product_id for product_id, _ in most_common_products]

import json
import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from core.database import engine, Base, SessionLocal
from core.log_config import log, log_decorator
from models.menu import MenuItem
from models.order import Order
from models.product import Product
from models.user import User


# Helper function to generate random dates
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


# Generate 1000 unique users
users_data = [
    {
        "name": f"User {i}",
        "email": f"user{i}@example.com",
        "phone": f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        "address": f"{random.randint(1, 999)} Main St",
        "is_active": True,
        "created_at": random_date(datetime(2023, 1, 1), datetime(2023, 12, 31)).strftime("%Y-%m-%d"),
        "rewards_points": random.randint(0, 500)
    }
    for i in range(1, 1001)
]

# Generate 1000 unique products
products_data = [
    {
        "name": f"Product {i}",
        "price": round(random.uniform(1.99, 99.99), 2),
        "stock": random.randint(1, 100),
        "description": f"Description for product {i}",
        "category": random.choice(["Food", "Drink", "Side", "Salad", "Dessert", "Main"]),
        "is_available": True,
        "tags": [random.choice(["tag1", "tag2", "tag3"]) for _ in range(3)]
    }
    for i in range(1, 1001)
]

# Generate 1000 unique menu items
menu_items_data = [
    {
        "name": f"MenuItem {i}",
        "description": f"Description for menu item {i}",
        "price": round(random.uniform(1.99, 99.99), 2),
        "category": random.choice(["Pizza", "Side", "Salad", "Dessert", "Drink", "Main"]),
        "is_vegetarian": random.choice([True, False]),
        "calories": random.randint(100, 1000),
        "is_gluten_free": random.choice([True, False]),
        "is_spicy": random.choice([True, False]),
        "is_available": True
    }
    for i in range(1, 101)
]

# Generate 1000 unique orders
orders_data = [
    {
        "user_id": random.randint(1, 1000),
        "product_ids": random.sample(range(1, 1001), k=random.randint(1, 5)),
        "total_price": round(random.uniform(10.00, 500.00), 2),
        "status": random.choice(["Pending", "Completed"]),
        "delivery_address": f"{random.randint(1, 999)} Main St",
        "order_date": random_date(datetime(2023, 1, 1), datetime(2023, 12, 31)).strftime("%Y-%m-%d"),
        "delivery_date": random_date(datetime(2023, 1, 1), datetime(2023, 12, 31)).strftime("%Y-%m-%d"),
        "rewards_points_used": random.randint(0, 50)
    }
    for i in range(1, 1001)
]


@log_decorator("INFO")
def create_fake_user(user_data):
    user = User(**user_data)
    log("INFO", f"Created user: {user.name}")
    return user


def create_fake_product(product_data):
    if 'tags' in product_data and isinstance(product_data['tags'], list):
        product_data['tags'] = ','.join(product_data['tags'])
    product = Product(**product_data)
    log("INFO", f"Created product: {product.name}")
    return product


@log_decorator("INFO")
def create_fake_order(order_data):
    order_data['product_ids'] = json.dumps(order_data['product_ids'])  # Serialize a list to JSON string
    order = Order(**order_data)
    log("INFO", f"Created order for user_id: {order.user_id}")
    return order


@log_decorator("INFO")
def create_fake_menu_item(menu_item_data):
    menu_item = MenuItem(**menu_item_data)
    log("INFO", f"Created menu item: {menu_item.name}")
    return menu_item


def populate_table(session: Session, model, data_list, create_fake_func):
    for data in data_list:
        session.add(create_fake_func(data))
    session.commit()
    log("INFO", f"Populated {len(data_list)} records in {model.__tablename__} table")


@log_decorator("INFO")
def main():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Populate users
        populate_table(db, User, users_data, create_fake_user)
        user_ids = [user.id for user in db.query(User.id).all()]

        # Populate products
        populate_table(db, Product, products_data, create_fake_product)
        product_ids = [product.id for product in db.query(Product.id).all()]

        # Populate orders
        for order_data in orders_data:
            order_data["user_id"] = random.choice(user_ids)
            order_data["product_ids"] = random.sample(product_ids, k=random.randint(1, len(product_ids)))
            db.add(create_fake_order(order_data))
        db.commit()

        # Populate menu items
        populate_table(db, MenuItem, menu_items_data, create_fake_menu_item)
    except Exception as e:
        log("ERROR", f"An error occurred during database population: {e}")
    finally:
        db.close()
        log("INFO", "Database session closed")


if __name__ == "__main__":
    main()

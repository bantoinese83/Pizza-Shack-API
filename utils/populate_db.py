import json
import random

from sqlalchemy.orm import Session

from core.database import engine, Base, SessionLocal
from core.log_config import log, log_decorator
from models.menu import MenuItem
from models.order import Order
from models.product import Product
from models.user import User

# Realistic data
users_data = [
    {"name": "John Doe", "email": "john.doe@example.com", "phone": "123-456-7890", "address": "123 Main St",
     "is_active": True, "created_at": "2023-10-01", "rewards_points": 100},
    {"name": "Jane Smith", "email": "jane.smith@example.com", "phone": "987-654-3210", "address": "456 Elm St",
     "is_active": True, "created_at": "2023-10-02", "rewards_points": 200},
    {"name": "Alice Johnson", "email": "alice.johnson@example.com", "phone": "555-123-4567", "address": "789 Oak St",
     "is_active": True, "created_at": "2023-10-03", "rewards_points": 150},
    {"name": "Bob Brown", "email": "bob.brown@example.com", "phone": "555-987-6543", "address": "321 Pine St",
     "is_active": True, "created_at": "2023-10-04", "rewards_points": 50},
    {"name": "Charlie Davis", "email": "charlie.davis@example.com", "phone": "555-654-3210", "address": "654 Maple St",
     "is_active": True, "created_at": "2023-10-05", "rewards_points": 75},
    {"name": "Diana Evans", "email": "diana.evans@example.com", "phone": "555-321-0987", "address": "987 Birch St",
     "is_active": True, "created_at": "2023-10-06", "rewards_points": 120},
    {"name": "Eve Foster", "email": "eve.foster@example.com", "phone": "555-876-5432", "address": "123 Cedar St",
     "is_active": True, "created_at": "2023-10-07", "rewards_points": 90},
    {"name": "Frank Green", "email": "frank.green@example.com", "phone": "555-432-1098", "address": "456 Spruce St",
     "is_active": True, "created_at": "2023-10-08", "rewards_points": 110},
    {"name": "Grace Harris", "email": "grace.harris@example.com", "phone": "555-098-7654", "address": "789 Willow St",
     "is_active": True, "created_at": "2023-10-09", "rewards_points": 130},
    {"name": "Henry Jackson", "email": "henry.jackson@example.com", "phone": "555-765-4321", "address": "321 Elm St",
     "is_active": True, "created_at": "2023-10-10", "rewards_points": 140},
    {"name": "Ivy King", "email": "ivy.king@example.com", "phone": "555-654-0987", "address": "654 Oak St",
     "is_active": True, "created_at": "2023-10-11", "rewards_points": 160},
    {"name": "Jack Lee", "email": "jack.lee@example.com", "phone": "555-321-8765", "address": "987 Pine St",
     "is_active": True, "created_at": "2023-10-12", "rewards_points": 170},
    {"name": "Karen Miller", "email": "karen.miller@example.com", "phone": "555-876-5432", "address": "123 Maple St",
     "is_active": True, "created_at": "2023-10-13", "rewards_points": 180},
    {"name": "Leo Nelson", "email": "leo.nelson@example.com", "phone": "555-432-1098", "address": "456 Birch St",
     "is_active": True, "created_at": "2023-10-14", "rewards_points": 190},
    {"name": "Mia Owens", "email": "mia.owens@example.com", "phone": "555-098-7654", "address": "789 Cedar St",
     "is_active": True, "created_at": "2023-10-15", "rewards_points": 200},
    {"name": "Nina Parker", "email": "nina.parker@example.com", "phone": "555-765-4321", "address": "321 Spruce St",
     "is_active": True, "created_at": "2023-10-16", "rewards_points": 210},
    {"name": "Oscar Quinn", "email": "oscar.quinn@example.com", "phone": "555-654-0987", "address": "654 Willow St",
     "is_active": True, "created_at": "2023-10-17", "rewards_points": 220},
    {"name": "Paula Roberts", "email": "paula.roberts@example.com", "phone": "555-321-8765", "address": "987 Elm St",
     "is_active": True, "created_at": "2023-10-18", "rewards_points": 230},
    {"name": "Quinn Scott", "email": "quinn.scott@example.com", "phone": "555-876-5432", "address": "123 Oak St",
     "is_active": True, "created_at": "2023-10-19", "rewards_points": 240},
    {"name": "Rachel Taylor", "email": "rachel.taylor@example.com", "phone": "555-432-1098", "address": "456 Pine St",
     "is_active": True, "created_at": "2023-10-20", "rewards_points": 250},
]

products_data = [
    {"name": "Cheese Pizza", "price": 9.99, "stock": 50, "description": "Delicious cheese pizza", "category": "Food",
     "is_available": True, "tags": ["cheese", "vegetarian"]},
    {"name": "Pepperoni Pizza", "price": 12.99, "stock": 30, "description": "Spicy pepperoni pizza", "category": "Food",
     "is_available": True, "tags": ["pepperoni", "spicy"]},
    {"name": "Veggie Pizza", "price": 11.99, "stock": 40, "description": "Healthy veggie pizza", "category": "Food",
     "is_available": True, "tags": ["vegetarian", "healthy"]},
    {"name": "BBQ Chicken Pizza", "price": 13.99, "stock": 25, "description": "BBQ chicken pizza", "category": "Food",
     "is_available": True, "tags": ["chicken", "bbq"]},
    {"name": "Hawaiian Pizza", "price": 14.99, "stock": 20, "description": "Pizza with pineapple and ham",
     "category": "Food",
     "is_available": True, "tags": ["pineapple", "ham"]},
    {"name": "Meat Lovers Pizza", "price": 15.99, "stock": 15, "description": "Pizza with various meats",
     "category": "Food",
     "is_available": True, "tags": ["meat", "hearty"]},
    {"name": "Margherita Pizza", "price": 8.99, "stock": 50, "description": "Classic Margherita pizza",
     "category": "Food",
     "is_available": True, "tags": ["classic", "vegetarian"]},
    {"name": "Buffalo Chicken Pizza", "price": 13.99, "stock": 25, "description": "Spicy buffalo chicken pizza",
     "category": "Food",
     "is_available": True, "tags": ["spicy", "chicken"]},
    {"name": "Supreme Pizza", "price": 16.99, "stock": 10, "description": "Pizza with all toppings", "category": "Food",
     "is_available": True, "tags": ["all", "hearty"]},
    {"name": "Four Cheese Pizza", "price": 12.99, "stock": 30, "description": "Pizza with four types of cheese",
     "category": "Food",
     "is_available": True, "tags": ["cheese", "vegetarian"]},
    {"name": "Garlic Bread", "price": 4.99, "stock": 100, "description": "Garlic bread sticks", "category": "Side",
     "is_available": True, "tags": ["garlic", "bread"]},
    {"name": "Chicken Wings", "price": 9.99, "stock": 50, "description": "Spicy chicken wings", "category": "Side",
     "is_available": True, "tags": ["chicken", "spicy"]},
    {"name": "Caesar Salad", "price": 7.99, "stock": 30, "description": "Classic Caesar salad", "category": "Salad",
     "is_available": True, "tags": ["salad", "healthy"]},
    {"name": "Greek Salad", "price": 8.99, "stock": 25, "description": "Greek salad with feta cheese",
     "category": "Salad",
     "is_available": True, "tags": ["salad", "vegetarian"]},
    {"name": "Chocolate Cake", "price": 6.99, "stock": 20, "description": "Rich chocolate cake", "category": "Dessert",
     "is_available": True, "tags": ["chocolate", "dessert"]},
    {"name": "Tiramisu", "price": 7.99, "stock": 15, "description": "Classic Italian dessert", "category": "Dessert",
     "is_available": True, "tags": ["dessert", "italian"]},
    {"name": "Lemonade", "price": 2.99, "stock": 100, "description": "Refreshing lemonade", "category": "Drink",
     "is_available": True, "tags": ["drink", "refreshing"]},
    {"name": "Iced Tea", "price": 2.99, "stock": 100, "description": "Cold iced tea", "category": "Drink",
     "is_available": True, "tags": ["drink", "refreshing"]},
    {"name": "Cola", "price": 1.99, "stock": 100, "description": "Classic cola drink", "category": "Drink",
     "is_available": True, "tags": ["drink", "classic"]},
    {"name": "Orange Juice", "price": 3.99, "stock": 50, "description": "Fresh orange juice", "category": "Drink",
     "is_available": True, "tags": ["drink", "healthy"]},
]

menu_items_data = [
    {"name": "Margherita", "description": "Classic cheese and tomato pizza", "price": 8.99, "category": "Pizza",
     "is_vegetarian": True, "calories": 250, "is_gluten_free": False, "is_spicy": False, "is_available": True},
    {"name": "BBQ Chicken", "description": "BBQ chicken pizza with onions and cilantro", "price": 11.99,
     "category": "Pizza", "is_vegetarian": False, "calories": 300, "is_gluten_free": False, "is_spicy": False,
     "is_available": True},
    {"name": "Pepperoni", "description": "Pepperoni pizza with mozzarella cheese", "price": 10.99, "category": "Pizza",
     "is_vegetarian": False, "calories": 280, "is_gluten_free": False, "is_spicy": False, "is_available": True},
    {"name": "Veggie Delight", "description": "Pizza with assorted vegetables", "price": 9.99, "category": "Pizza",
     "is_vegetarian": True, "calories": 240, "is_gluten_free": False, "is_spicy": False, "is_available": True},
    {"name": "Hawaiian", "description": "Pizza with ham and pineapple", "price": 12.99, "category": "Pizza",
     "is_vegetarian": False, "calories": 260, "is_gluten_free": False, "is_spicy": False, "is_available": True},
    {"name": "Meat Lovers", "description": "Pizza with various meats", "price": 14.99, "category": "Pizza",
     "is_vegetarian": False, "calories": 320, "is_gluten_free": False, "is_spicy": False, "is_available": True},
    {"name": "Four Cheese", "description": "Pizza with four types of cheese", "price": 11.99, "category": "Pizza",
     "is_vegetarian": True, "calories": 270, "is_gluten_free": False, "is_spicy": False, "is_available": True},
    {"name": "Buffalo Chicken", "description": "Spicy buffalo chicken pizza", "price": 13.99, "category": "Pizza",
     "is_vegetarian": False, "calories": 290, "is_gluten_free": False, "is_spicy": True, "is_available": True},
    {"name": "Supreme", "description": "Pizza with all toppings", "price": 15.99, "category": "Pizza",
     "is_vegetarian": False, "calories": 350, "is_gluten_free": False, "is_spicy": False, "is_available": True},
    {"name": "Garlic Bread", "description": "Garlic bread sticks", "price": 4.99, "category": "Side",
     "is_vegetarian": True, "calories": 150, "is_gluten_free": False, "is_spicy": False, "is_available": True},
    {"name": "Chicken Wings", "description": "Spicy chicken wings", "price": 9.99, "category": "Side",
     "is_vegetarian": False, "calories": 200, "is_gluten_free": False, "is_spicy": True, "is_available": True},
    {"name": "Caesar Salad", "description": "Classic Caesar salad", "price": 7.99, "category": "Salad",
     "is_vegetarian": False, "calories": 180, "is_gluten_free": False, "is_spicy": False, "is_available": True},
    {"name": "Greek Salad", "description": "Greek salad with feta cheese", "price": 8.99, "category": "Salad",
     "is_vegetarian": True, "calories": 160, "is_gluten_free": False, "is_spicy": False, "is_available": True},
    {"name": "Chocolate Cake", "description": "Rich chocolate cake", "price": 6.99, "category": "Dessert",
     "is_vegetarian": True, "calories": 300, "is_gluten_free": False, "is_spicy": False, "is_available": True},
    {"name": "Tiramisu", "description": "Classic Italian dessert", "price": 7.99, "category": "Dessert",
     "is_vegetarian": True, "calories": 320, "is_gluten_free": False, "is_spicy": False, "is_available": True},
    {"name": "Lemonade", "description": "Refreshing lemonade", "price": 2.99, "category": "Drink",
     "is_vegetarian": True, "calories": 100, "is_gluten_free": True, "is_spicy": False, "is_available": True},
    {"name": "Iced Tea", "description": "Cold iced tea", "price": 2.99, "category": "Drink",
     "is_vegetarian": True, "calories": 90, "is_gluten_free": True, "is_spicy": False, "is_available": True},
    {"name": "Cola", "description": "Classic cola drink", "price": 1.99, "category": "Drink",
     "is_vegetarian": True, "calories": 110, "is_gluten_free": True, "is_spicy": False, "is_available": True},
    {"name": "Orange Juice", "description": "Fresh orange juice", "price": 3.99, "category": "Drink",
     "is_vegetarian": True, "calories": 120, "is_gluten_free": True, "is_spicy": False, "is_available": True},
    {"name": "BBQ Ribs", "description": "BBQ ribs with sauce", "price": 15.99, "category": "Main",
     "is_vegetarian": False, "calories": 400, "is_gluten_free": False, "is_spicy": False, "is_available": True},
]

orders_data = [
    {"user_id": 1, "product_ids": [1, 2], "total_price": 22.98, "status": "Pending", "delivery_address": "123 Main St",
     "order_date": "2023-10-01", "delivery_date": "2023-10-02", "rewards_points_used": 10},
    {"user_id": 2, "product_ids": [2], "total_price": 12.99, "status": "Completed", "delivery_address": "456 Elm St",
     "order_date": "2023-10-02", "delivery_date": "2023-10-03", "rewards_points_used": 20},
    {"user_id": 3, "product_ids": [3, 4], "total_price": 25.98, "status": "Pending", "delivery_address": "789 Oak St",
     "order_date": "2023-10-03", "delivery_date": "2023-10-04", "rewards_points_used": 15},
    {"user_id": 4, "product_ids": [1, 3], "total_price": 18.99, "status": "Completed",
     "delivery_address": "321 Pine St",
     "order_date": "2023-10-04", "delivery_date": "2023-10-05", "rewards_points_used": 5},
    {"user_id": 5, "product_ids": [2, 4], "total_price": 27.98, "status": "Pending", "delivery_address": "654 Maple St",
     "order_date": "2023-10-05", "delivery_date": "2023-10-06", "rewards_points_used": 0},
    {"user_id": 6, "product_ids": [1, 4], "total_price": 19.98, "status": "Completed",
     "delivery_address": "987 Birch St",
     "order_date": "2023-10-06", "delivery_date": "2023-10-07", "rewards_points_used": 10},
    {"user_id": 7, "product_ids": [3], "total_price": 14.99, "status": "Pending", "delivery_address": "159 Cedar St",
     "order_date": "2023-10-07", "delivery_date": "2023-10-08", "rewards_points_used": 20},
    {"user_id": 8, "product_ids": [2, 3, 4], "total_price": 35.97, "status": "Completed",
     "delivery_address": "753 Walnut St",
     "order_date": "2023-10-08", "delivery_date": "2023-10-09", "rewards_points_used": 15},
    {"user_id": 9, "product_ids": [1, 2, 3], "total_price": 32.97, "status": "Pending",
     "delivery_address": "852 Chestnut St",
     "order_date": "2023-10-09", "delivery_date": "2023-10-10", "rewards_points_used": 25},
    {"user_id": 10, "product_ids": [4], "total_price": 9.99, "status": "Completed", "delivery_address": "951 Spruce St",
     "order_date": "2023-10-10", "delivery_date": "2023-10-11", "rewards_points_used": 5},
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
    order_data['product_ids'] = json.dumps(order_data['product_ids'])  # Serialize list to JSON string
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

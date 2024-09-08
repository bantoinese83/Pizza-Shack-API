from fastapi import APIRouter, HTTPException

from core.log_config import log_decorator, spinner_decorator
from models.order import Order, orders
from models.product import products
from models.user import users

router = APIRouter()


@router.get("/orders", description="Fetch all orders")
@log_decorator("INFO")
@spinner_decorator("Fetching all orders")
async def get_orders():
    return orders


@router.post("/orders/", response_model=Order, description="Create a new order")
@log_decorator("INFO")
@spinner_decorator("Creating order")
async def create_order(order: Order):
    if not any(u.id == order.user_id for u in users):
        raise HTTPException(status_code=404, detail="User not found")
    total_price = 0
    for product_id in order.product_ids:
        product = next((p for p in products if p.id == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.stock <= 0:
            raise HTTPException(status_code=400, detail=f"Product {product.name} is out of stock")
        total_price += product.price
        product.stock -= 1
    order.total_price = total_price
    order.status = "Pending"
    orders.append(order)
    return order


@router.get("/orders/{order_id}", response_model=Order, description="Fetch order by ID")
@log_decorator("INFO")
@spinner_decorator("Fetching order")
async def get_order(order_id: int):
    order = next((order for order in orders if order.id == order_id), None)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/orders/{order_id}", response_model=Order, description="Update order by ID")
@log_decorator("INFO")
@spinner_decorator("Updating order")
async def update_order(order_id: int, updated_order: Order):
    order = next((order for order in orders if order.id == order_id), None)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    updated_order.id = order_id
    orders[orders.index(order)] = updated_order
    return updated_order


@router.delete("/orders/{order_id}", response_model=Order, description="Delete order by ID")
@log_decorator("INFO")
@spinner_decorator("Deleting order")
async def delete_order(order_id: int):
    order = next((order for order in orders if order.id == order_id), None)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    orders.remove(order)
    return order


@router.get("/users/{user_id}/orders", response_model=list[Order], description="Fetch orders by user ID")
@log_decorator("INFO")
@spinner_decorator("Fetching orders by user ID")
async def get_orders_by_user(user_id: int):
    user_orders = [order for order in orders if order.user_id == user_id]
    if not user_orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return user_orders

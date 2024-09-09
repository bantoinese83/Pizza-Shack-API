# api/orders.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from api.dep import get_db
from core.log_config import log_decorator, spinner_decorator
from crud.order import get_orders, get_order, create_order as crud_create_order, update_order, delete_order
from schemas.order import Order as OrderSchema

router = APIRouter()


@router.get("/orders", description="Fetch all orders")
@log_decorator("INFO")
@spinner_decorator("Fetching all orders")
async def get_all_orders(db: Session = Depends(get_db)):
    return get_orders(db)


@router.post("/orders/", response_model=OrderSchema, description="Create a new order")
@log_decorator("INFO")
@spinner_decorator("Creating order")
async def create_new_order(order: OrderSchema, db: Session = Depends(get_db)):
    return crud_create_order(db, order)


@router.get("/orders/{order_id}", response_model=OrderSchema, description="Fetch order by ID")
@log_decorator("INFO")
@spinner_decorator("Fetching order")
async def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/orders/{order_id}", response_model=OrderSchema, description="Update order by ID")
@log_decorator("INFO")
@spinner_decorator("Updating order")
async def update_order_by_id(order_id: int, updated_order: OrderSchema, db: Session = Depends(get_db)):
    order = get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return update_order(db, order_id, updated_order)


@router.delete("/orders/{order_id}", response_model=OrderSchema, description="Delete order by ID")
@log_decorator("INFO")
@spinner_decorator("Deleting order")
async def delete_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return delete_order(db, order_id)

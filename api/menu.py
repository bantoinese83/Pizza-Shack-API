from fastapi import APIRouter, HTTPException

from core.log_config import log_decorator, spinner_decorator
from models.menu import MenuItem, menu_items

router = APIRouter()


@router.get("/menu", description="Fetch all menu items")
@log_decorator("INFO")
@spinner_decorator("Fetching menu items")
async def get_menu():
    return menu_items


@router.get("/menu/{item_id}", description="Fetch menu item by ID")
@log_decorator("INFO")
@spinner_decorator("Fetching menu item")
async def get_menu_item(item_id: int):
    item = next((item for item in menu_items if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/menu", description="Add a new menu item")
@log_decorator("INFO")
@spinner_decorator("Adding new menu item")
async def add_menu_item(item: MenuItem):
    item.id = len(menu_items) + 1
    menu_items.append(item)
    return item


@router.put("/menu/{item_id}", description="Update menu item by ID")
@log_decorator("INFO")
@spinner_decorator("Updating menu item")
async def update_menu_item(item_id: int, updated_item: MenuItem):
    item = next((item for item in menu_items if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item.id = item_id
    menu_items[menu_items.index(item)] = updated_item
    return updated_item


@router.delete("/menu/{item_id}", description="Delete menu item by ID")
@log_decorator("INFO")
@spinner_decorator("Deleting menu item")
async def delete_menu_item(item_id: int):
    item = next((item for item in menu_items if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    menu_items.remove(item)
    return item


@router.get("/menu/name/{name}", description="Fetch menu items by name")
@log_decorator("INFO")
@spinner_decorator("Fetching menu items by name")
async def get_menu_items_by_name(name: str):
    items = [item for item in menu_items if name.lower() in item.name.lower()]
    if not items:
        raise HTTPException(status_code=404, detail="No items found with that name")
    return items


@router.get("/menu/price/", description="Fetch menu items by price range")
@log_decorator("INFO")
@spinner_decorator("Fetching menu items by price range")
async def get_menu_items_by_price(min_price: float, max_price: float):
    items = [item for item in menu_items if min_price <= item.price <= max_price]
    if not items:
        raise HTTPException(status_code=404, detail="No items found in that price range")
    return items

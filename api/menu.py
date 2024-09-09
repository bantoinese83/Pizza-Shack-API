from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from api.dep import get_db
from core.log_config import log_decorator, spinner_decorator
from crud.menu import get_menu_items, get_menu_item, create_menu_item, update_menu_item, delete_menu_item
from schemas.menu import MenuItem as MenuItemSchema

router = APIRouter()


@router.get("/menu", description="Fetch all menu items")
@log_decorator("INFO")
@spinner_decorator("Fetching menu items")
async def get_menu(db: Session = Depends(get_db)):
    return get_menu_items(db)


@router.get("/menu/{item_id}", description="Fetch menu item by ID")
@log_decorator("INFO")
@spinner_decorator("Fetching menu item")
async def get_menu_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    item = get_menu_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/menu", description="Add a new menu item")
@log_decorator("INFO")
@spinner_decorator("Adding new menu item")
async def add_menu_item(item: MenuItemSchema, db: Session = Depends(get_db)):
    return create_menu_item(db, item)


@router.put("/menu/{item_id}", description="Update menu item by ID")
@log_decorator("INFO")
@spinner_decorator("Updating menu item")
async def update_menu_item_endpoint(item_id: int, updated_item: MenuItemSchema, db: Session = Depends(get_db)):
    item = get_menu_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return update_menu_item(db, item_id, updated_item)


@router.delete("/menu/{item_id}", description="Delete menu item by ID")
@log_decorator("INFO")
@spinner_decorator("Deleting menu item")
async def delete_menu_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    item = get_menu_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return delete_menu_item(db, item_id)

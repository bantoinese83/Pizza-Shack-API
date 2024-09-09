from sqlalchemy.orm import Session
from models.menu import MenuItem
from schemas.menu import MenuItem as MenuItemSchema

def get_menu_items(db: Session):
    return db.query(MenuItem).all()

def get_menu_item(db: Session, item_id: int):
    return db.query(MenuItem).filter(MenuItem.id == item_id).first()

def create_menu_item(db: Session, menu_item: MenuItemSchema):
    db_menu_item = MenuItem(**menu_item.dict())
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

def update_menu_item(db: Session, item_id: int, menu_item: MenuItemSchema):
    db_menu_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if db_menu_item:
        for key, value in menu_item.dict().items():
            setattr(db_menu_item, key, value)
        db.commit()
        db.refresh(db_menu_item)
    return db_menu_item

def delete_menu_item(db: Session, item_id: int):
    db_menu_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if db_menu_item:
        db.delete(db_menu_item)
        db.commit()
    return db_menu_item
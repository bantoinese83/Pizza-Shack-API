from sqlalchemy.orm import Session

from models.product import Product
from schemas.product import Product as ProductSchema


def get_products(db: Session):
    db_products = db.query(Product).all()
    for db_product in db_products:
        if db_product.tags:
            db_product.tags = db_product.tags.split(',')
    return db_products


def get_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product and db_product.tags:
        db_product.tags = db_product.tags.split(',')
    return db_product


def create_product(db: Session, product: ProductSchema):
    product_data = product.dict()
    if product_data.get('tags'):
        product_data['tags'] = ','.join(product_data['tags'])
    db_product = Product(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    if db_product.tags:
        db_product.tags = db_product.tags.split(',')
    return db_product


def update_product(db: Session, product_id: int, product: ProductSchema):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        product_data = product.dict()
        if product_data.get('tags'):
            product_data['tags'] = ','.join(product_data['tags'])
        for key, value in product_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        if db_product.tags:
            db_product.tags = db_product.tags.split(',')
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
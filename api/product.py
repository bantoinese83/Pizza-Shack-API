from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from api.dep import get_db
from core.log_config import log_decorator, spinner_decorator
from crud.product import get_products, get_product, create_product, update_product, delete_product
from schemas.product import Product as ProductSchema

router = APIRouter()


@router.post("/products/", response_model=ProductSchema, description="Create a new product")
@log_decorator("INFO")
@spinner_decorator("Creating product")
async def create_product_endpoint(product: ProductSchema, db: Session = Depends(get_db)):
    return create_product(db, product)


@router.get("/products/", response_model=list[ProductSchema], description="Fetch all products")
@log_decorator("INFO")
@spinner_decorator("Fetching all products")
async def get_products_endpoint(db: Session = Depends(get_db)):
    return get_products(db)


@router.get("/products/{product_id}", response_model=ProductSchema, description="Fetch product by ID")
@log_decorator("INFO")
@spinner_decorator("Fetching product")
async def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{product_id}", response_model=ProductSchema, description="Update product by ID")
@log_decorator("INFO")
@spinner_decorator("Updating product")
async def update_product_endpoint(product_id: int, updated_product: ProductSchema, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return update_product(db, product_id, updated_product)


@router.delete("/products/{product_id}", response_model=ProductSchema, description="Delete product by ID")
@log_decorator("INFO")
@spinner_decorator("Deleting product")
async def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return delete_product(db, product_id)

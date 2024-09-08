from fastapi import APIRouter, HTTPException

from core.log_config import log_decorator, spinner_decorator
from models.product import Product, products

router = APIRouter()


@router.post("/products/", response_model=Product, description="Create a new product")
@log_decorator("INFO")
@spinner_decorator("Creating product")
async def create_product(product: Product):
    if any(p.id == product.id for p in products):
        raise HTTPException(status_code=400, detail="Product already exists")
    products.append(product)
    return product


@router.get("/products/", response_model=list[Product], description="Fetch all products")
@log_decorator("INFO")
@spinner_decorator("Fetching all products")
async def get_products():
    return products


@router.get("/products/{product_id}", response_model=Product, description="Fetch product by ID")
@log_decorator("INFO")
@spinner_decorator("Fetching product")
async def get_product(product_id: int):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{product_id}", response_model=Product, description="Update product by ID")
@log_decorator("INFO")
@spinner_decorator("Updating product")
async def update_product(product_id: int, updated_product: Product):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product.id = product_id
    products[products.index(product)] = updated_product
    return updated_product


@router.delete("/products/{product_id}", response_model=Product, description="Delete product by ID")
@log_decorator("INFO")
@spinner_decorator("Deleting product")
async def delete_product(product_id: int):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    products.remove(product)
    return product

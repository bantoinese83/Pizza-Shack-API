from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.dep import get_db
from core.log_config import log_decorator, spinner_decorator
from crud.product import get_product
from crud.recommendations import recommend_products
from crud.user import get_user

router = APIRouter()


@router.get("/recommendations", description="Get product recommendations based on past orders")
@log_decorator("INFO")
@spinner_decorator("Fetching recommendations")
async def get_recommendations(top_n: int = Query(5, ge=1, le=100), db: Session = Depends(get_db)):
    try:
        recommendations = recommend_products(db, top_n)
        return {"recommended_product_ids": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching recommendations: {e}")


@router.get("/recommendations/user/{user_id}", description="Get product recommendations for a specific user")
@log_decorator("INFO")
@spinner_decorator("Fetching user recommendations")
async def get_user_recommendations(user_id: int, top_n: int = Query(5, ge=1, le=100), db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        recommendations = recommend_products(db, top_n, user_id=user_id)
        return {"recommended_product_ids": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching user recommendations: {e}")


@router.get("/recommendations/product/{product_id}",
            description="Get product recommendations based on a specific product")
@log_decorator("INFO")
@spinner_decorator("Fetching product recommendations")
async def get_product_recommendations(product_id: int, top_n: int = Query(5, ge=1, le=100),
                                      db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    try:
        recommendations = recommend_products(db, top_n, product_id=product_id)
        return {"recommended_product_ids": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching product recommendations: {e}")


@router.get("/recommendations/category/{category}",
            description="Get product recommendations based on a specific category")
@log_decorator("INFO")
@spinner_decorator("Fetching category recommendations")
async def get_category_recommendations(category: str, top_n: int = Query(5, ge=1, le=100),
                                       db: Session = Depends(get_db)):
    try:
        recommendations = recommend_products(db, top_n, category=category)
        return {"recommended_product_ids": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching category recommendations: {e}")

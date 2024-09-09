# api/users.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from api.dep import get_db
from core.log_config import log_decorator, spinner_decorator
from crud.user import get_users, get_user, create_user, update_user, delete_user
from schemas.user import User as UserSchema

router = APIRouter()


@router.get("/users", response_model=list[UserSchema], description="Fetch all users")
@log_decorator("INFO")
@spinner_decorator("Fetching all users")
async def get_all_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.post("/users/", response_model=UserSchema, description="Create a new user")
@log_decorator("INFO")
@spinner_decorator("Creating user")
async def create_new_user(user: UserSchema, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/users/{user_id}", response_model=UserSchema, description="Fetch user by ID")
@log_decorator("INFO")
@spinner_decorator("Fetching user")
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserSchema, description="Update user by ID")
@log_decorator("INFO")
@spinner_decorator("Updating user")
async def update_user_by_id(user_id: int, updated_user: UserSchema, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(db, user_id, updated_user)


@router.delete("/users/{user_id}", response_model=UserSchema, description="Delete user by ID")
@log_decorator("INFO")
@spinner_decorator("Deleting user")
async def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return delete_user(db, user_id)
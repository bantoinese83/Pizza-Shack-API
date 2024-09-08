from fastapi import APIRouter, HTTPException

from core.log_config import log_decorator, spinner_decorator
from models.user import User, users

router = APIRouter()


@router.post("/users/", response_model=User, description="Create a new user")
@log_decorator("INFO")
@spinner_decorator("Creating user")
async def create_user(user: User):
    if any(u.id == user.id for u in users):
        raise HTTPException(status_code=400, detail="User already exists")
    users.append(user)
    return user


@router.get("/users/", response_model=list[User], description="Fetch all users")
@log_decorator("INFO")
@spinner_decorator("Fetching all users")
async def get_users():
    return users


@router.get("/users/{user_id}", response_model=User, description="Fetch user by ID")
@log_decorator("INFO")
@spinner_decorator("Fetching user")
async def get_user(user_id: int):
    user = next((u for u in users if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=User, description="Update user by ID")
@log_decorator("INFO")
@spinner_decorator("Updating user")
async def update_user(user_id: int, updated_user: User):
    user = next((u for u in users if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user.id = user_id
    users[users.index(user)] = updated_user
    return updated_user


@router.delete("/users/{user_id}", response_model=User, description="Delete user by ID")
@log_decorator("INFO")
@spinner_decorator("Deleting user")
async def delete_user(user_id: int):
    user = next((u for u in users if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    users.remove(user)
    return user

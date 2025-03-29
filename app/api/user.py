# app/api/users.py

from fastapi import APIRouter
from app.services import user_service

router = APIRouter()

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    return await user_service.get_user_by_id(user_id)

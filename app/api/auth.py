# app/api/auth.py

from fastapi import APIRouter, HTTPException, Depends
from app.services import auth_service

router = APIRouter()

@router.post("/signup")
async def sign_up(email: str, password: str):
    return await auth_service.sign_up(email, password)

@router.post("/login")
async def login(email: str, password: str):
    return await auth_service.login(email, password)

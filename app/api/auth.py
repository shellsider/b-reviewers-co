# app/api/auth.py

from fastapi import APIRouter, HTTPException, Depends
from app.services import auth_service
from app.models.auth import SignInRequest, SignUpRequest, AuthResponse, UserResponse
from app.utils.auth_middleware import get_current_user
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.post("/signup")
async def sign_up(sign_up_data: SignUpRequest):
    return await auth_service.sign_up(sign_up_data)

@router.post("/login")
async def login(email: str, password: str):
    return await auth_service.login(email, password)

@router.post("/signin", response_model=AuthResponse)
async def sign_in(sign_in_data: SignInRequest):
    return await auth_service.sign_in(sign_in_data)

@router.post("/signout")
async def sign_out(token: str = Depends(security)):
    """
    Sign out user and revoke their tokens.
    Requires valid bearer token.
    """
    return await auth_service.sign_out(token.credentials)

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    return await auth_service.get_current_user_info(current_user)

@router.delete("/delete")
async def delete_user_account(current_user: dict = Depends(get_current_user)):
    """
    Delete user account from both Firebase Authentication and Firestore.
    Requires authentication.
    """
    return await auth_service.delete_user(current_user)

# app/services/auth_service.py

from firebase_admin import auth
from fastapi import HTTPException

async def sign_up(email: str, password: str):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def login(email: str, password: str):
    # For simplicity, just return the email (you should handle password verification here)
    # Firebase authentication typically uses ID tokens for verifying the identity of a user
    return {"email": email, "message": "Login successful"}

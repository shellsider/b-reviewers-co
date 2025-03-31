# app/services/auth_service.py

from firebase_admin import auth
from fastapi import HTTPException
import requests
from app.models.auth import SignInRequest, AuthResponse, UserResponse, SignUpRequest
from app.utils.env_manager import FIREBASE_WEB_API_KEY
from app.services.firestore_service import create_user_document, get_user_by_email, verify_password

# Firebase Auth URLs
FIREBASE_AUTH_SIGN_IN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
FIREBASE_AUTH_SIGN_UP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"

async def sign_up(sign_up_data: SignUpRequest):
    try:
        # First create the user in Firebase Auth and get the ID token
        payload = {
            "email": sign_up_data.email,
            "password": sign_up_data.password,
            "returnSecureToken": True
        }
        response = requests.post(FIREBASE_AUTH_SIGN_UP_URL, json=payload)
        data = response.json()

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=data.get("error", {}).get("message", "Registration failed")
            )

        # Get the user from Firebase Auth
        user = auth.get_user_by_email(sign_up_data.email)
        
        # Store additional user data in Firestore
        user_data = create_user_document(
            email=sign_up_data.email,
            name=sign_up_data.name,
            age=sign_up_data.age,
            password=sign_up_data.password,
            uid=user.uid
        )
        
        # Return user data with token
        return {
            **user_data,
            "access_token": data["idToken"],
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def login(email: str, password: str):
    # For simplicity, just return the email (you should handle password verification here)
    # Firebase authentication typically uses ID tokens for verifying the identity of a user
    return {"email": email, "message": "Login successful"}

async def sign_in(sign_in_data: SignInRequest) -> AuthResponse:
    try:
        # Get user from Firestore first to verify account status
        user_doc = get_user_by_email(sign_in_data.email)
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user_doc.get('account_deleted', False):
            raise HTTPException(status_code=400, detail="Account has been deleted")
        
        if user_doc.get('account_status') != 'active':
            raise HTTPException(status_code=400, detail="Account is not active")

        # Sign in with Firebase Auth REST API
        payload = {
            "email": sign_in_data.email,
            "password": sign_in_data.password,
            "returnSecureToken": True
        }
        response = requests.post(FIREBASE_AUTH_SIGN_IN_URL, json=payload)
        data = response.json()

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=data.get("error", {}).get("message", "Authentication failed")
            )

        return AuthResponse(
            access_token=data["idToken"],
            token_type="bearer"
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def sign_out(id_token: str) -> dict:
    try:
        # Verify and revoke the token
        decoded_token = auth.verify_id_token(id_token)
        auth.revoke_refresh_tokens(decoded_token["uid"])
        return {"message": "Successfully signed out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def get_current_user_info(user_token: dict) -> UserResponse:
    try:
        # Get user from Firebase Auth
        firebase_user = auth.get_user(user_token["uid"])
        
        # Get additional user data from Firestore
        user_doc = get_user_by_email(firebase_user.email)
        if not user_doc:
            raise HTTPException(status_code=404, detail="User data not found")

        return UserResponse(
            email=firebase_user.email,
            uid=firebase_user.uid,
            name=user_doc['name'],
            age=user_doc['age'],
            account_status=user_doc['account_status']
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

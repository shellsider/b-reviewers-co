# app/services/user_service.py

from app.firebase import db
from app.models import user
from fastapi import HTTPException

async def get_user_by_id(user_id: str):
    try:
        user_ref = db.collection("users").document(user_id)
        doc = user_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def create_user(user_data: user.User):
    try:
        user_ref = db.collection("users").document(user_data.id)
        user_ref.set(user_data.dict())
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# app/main.py

from fastapi import FastAPI
from app.api import auth
from app.firebase import db  # This will ensure Firebase is initialized at startup

app = FastAPI()

# Include the auth router
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Firebase!"}

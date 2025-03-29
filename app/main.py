# app/main.py

from fastapi import FastAPI
from app.api import auth, users

app = FastAPI()

# Include the routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Firebase!"}

# app/firebase.py

import firebase_admin
from firebase_admin import credentials, firestore
from app.utils.env_manager import FIREBASE_ADMIN_SDK_PATH

# Initialize Firebase Admin SDK using the credentials path from environment variables
cred = credentials.Certificate(FIREBASE_ADMIN_SDK_PATH)
firebase_admin.initialize_app(cred)

# Firebase Firestore reference
db = firestore.client()

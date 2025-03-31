from firebase_admin import firestore
import bcrypt
from fastapi import HTTPException
from app.firebase import db  # Import the already initialized db instance

users_collection = db.collection('users')

def create_user_document(email: str, name: str, age: int, password: str, uid: str) -> dict:
    try:
        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Create user document data
        user_data = {
            'email': email,
            'name': name,
            'age': age,
            'uid': uid,  # Store the Firebase UID
            'hashed_password': hashed_password.decode('utf-8'),  # Store as string
            'account_status': 'active',
            'account_deleted': False
        }
        
        # Use email as document ID
        users_collection.document(email).set(user_data)
        
        # Return user data without sensitive information
        return {
            'email': email,
            'name': name,
            'age': age,
            'uid': uid,
            'account_status': 'active'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user document: {str(e)}")

def get_user_by_email(email: str) -> dict:
    try:
        doc = users_collection.document(email).get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user document: {str(e)}")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying password: {str(e)}")

def update_user_status(email: str, status: str) -> dict:
    try:
        users_collection.document(email).update({
            'account_status': status
        })
        return {'message': f'User status updated to {status}'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user status: {str(e)}")

def delete_user_document(email: str) -> dict:
    try:
        # Get the document reference
        doc_ref = users_collection.document(email)
        
        # Check if document exists
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="User not found in Firestore")
        
        # Delete the document
        doc_ref.delete()
        
        return {'message': f'User document for {email} successfully deleted from Firestore'}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user document: {str(e)}") 
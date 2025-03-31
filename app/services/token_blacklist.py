from firebase_admin import firestore
from app.firebase import db
from datetime import datetime

blacklist_collection = db.collection('token_blacklist')

def add_to_blacklist(token: str, uid: str) -> None:
    """Add a token to the blacklist"""
    blacklist_collection.document(token).set({
        'uid': uid,
        'revoked_at': datetime.utcnow(),
        'token': token
    })

def is_token_blacklisted(token: str) -> bool:
    """Check if a token is blacklisted"""
    doc = blacklist_collection.document(token).get()
    return doc.exists

def cleanup_blacklist() -> None:
    """
    Clean up expired tokens from blacklist
    Note: This should be run periodically in a production environment
    """
    # Implementation for cleanup can be added later
    pass 
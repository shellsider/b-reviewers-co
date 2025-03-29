# app/utils/env_manager.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_env_variable(key: str, default=None):
    """
    Get an environment variable, or return a default value if not set.
    """
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Environment variable '{key}' is required but not set.")
    return value

# Firebase Credentials (Accessing via environment variables)
FIREBASE_ADMIN_SDK_PATH = get_env_variable("FIREBASE_ADMIN_SDK_PATH")

import bcrypt
from core.config import settings

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hash_password: str) -> str:
    return bcrypt.checkpw(password.encode(), hash_password.encode())

def create
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import jwt
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

from models.user import UserModel
from database.user_queries import get_user_via_email

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    if SECRET_KEY is None:
        raise ValueError("SECRET_KEY is not set in the environment variables.")
    data.update(
        {"exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) }
    )
    secret_bytes = SECRET_KEY.encode("utf-8")
    encoded_jwt = jwt.encode(data, secret_bytes, algorithm=ALGORITHM) 
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str) -> UserModel | None:
    user = get_user_via_email(email, db)
    if not user or not pwd_context.verify(password, user.password_hash):
        return None
    return user


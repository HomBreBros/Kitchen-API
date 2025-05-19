from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv
import bcrypt

from models.user import UserModel
from database.user_queries import get_user_via_email

load_dotenv()
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])

def create_access_token(data: dict):
    if SECRET_KEY is None:
        raise ValueError("SECRET_KEY is not set in the environment variables.")
    data.update(
        {"exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) }
    )
    secret_bytes = SECRET_KEY.encode("utf-8")
    encoded_jwt = jwt.encode(data, secret_bytes, algorithm=ALGORITHM) 
    return encoded_jwt

def decode_jwt(authorization: str) -> str:
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise JWTError

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return email

def authenticate_user(db: Session, email: str, password: str) -> UserModel | None:
    user = get_user_via_email(email, db)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
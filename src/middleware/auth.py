from fastapi import HTTPException, Request, status
from dotenv import load_dotenv
import os

from database.user_queries import get_user_via_email
from database.database import SessionLocal
from utils import decode_jwt

load_dotenv()

async def authenticate(request: Request, call_next):
    if request.url.path in ["/login", "/register", "/docs", "/openapi.json"]:
        return await call_next(request)

    authorization = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    db = SessionLocal()

    email = decode_jwt(authorization)
    user = get_user_via_email(email, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    request.state.user = user
    response = await call_next(request)

    db.close() 
    
    return response
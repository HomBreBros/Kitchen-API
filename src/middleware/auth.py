from fastapi import HTTPException, Request, status
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

from database.user_queries import get_user_via_email
from database.database import get_db, SessionLocal

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "xxxx")
ALGORITHM = "HS256"

async def authenticate(request: Request, call_next):
    if request.url.path == "/login" or request.url.path == "/register":
        return await call_next(request)

    authorization = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    db = SessionLocal()

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise JWTError
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
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
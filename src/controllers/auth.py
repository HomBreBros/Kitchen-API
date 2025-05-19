from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database.database import get_db

from db_models.user_model import User
from database.user_queries import get_user_via_email
from models.user import Token, LoginModel, CreateUser
from utils import create_access_token, authenticate_user


login_router = APIRouter(tags=["login"])
                        
@login_router.post("/register", status_code=201)
def register(user: CreateUser, session: Session = Depends(get_db)):
    print("Creating user:", user)
    existing_user = get_user_via_email(user.email, session)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"user": new_user}

@login_router.post("/login", response_model=Token)
async def login(login: LoginModel, db: Session = Depends(get_db)):
    user = authenticate_user(db, login.email, login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

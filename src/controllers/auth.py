from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database.database import get_db
import bcrypt

from db_models.user_model import User
from database.user_queries import get_user_via_email
from models.user import Token, LoginModel, CreateUser, UserModel
from utils import create_access_token, authenticate_user


login_router = APIRouter(tags=["login"])
                        
@login_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: CreateUser, session: Session = Depends(get_db)):
    existing_user = get_user_via_email(user.email, session)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    bcrypt_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt_salt).decode('utf-8')
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return UserModel.model_validate(new_user)

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
    return Token(
        access_token=access_token,
        token_type="bearer"
    )

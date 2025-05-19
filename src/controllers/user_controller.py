from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi import Depends

from database.database import get_db
from models.user import LoginModel

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("")
async def get_user(request: Request):
    user = request.state.user
    return user
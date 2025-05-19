from fastapi import APIRouter, Request

from models.user import UserModel

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("", response_model=UserModel)
async def get_user(request: Request):
    user = request.state.user
    return user
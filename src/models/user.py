from pydantic import BaseModel
from datetime import datetime

class UserModel(BaseModel):
    id: int
    name: str
    email: str
    password_hash: str
    created_at: datetime

    class Config:
        from_orm = True
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginModel(BaseModel):
    email: str
    password: str

class CreateUser(BaseModel):
    name: str
    email: str
    password: str
from sqlalchemy.orm import Session

from db_models.user_model import User
from models.user import UserModel

from sqlalchemy import select

def get_user_via_email(email: str, db: Session) -> UserModel | None:
    query = select(User).where(User.email == email)
    user = db.execute(query).scalar_one_or_none()

    return UserModel.model_validate(user) if user else None
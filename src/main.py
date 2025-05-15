from fastapi import FastAPI

from database.database import db_session
from models.user_model import User

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.middleware("http")
# def auth():
#    print("add auth here")


@app.get("/users")
def get_users():
    session = db_session()
    users = session.query(User).all()
    return {"users": users}

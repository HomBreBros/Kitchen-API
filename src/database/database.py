import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()
username = os.getenv("username")
password = os.getenv("password")
host = os.getenv("hostname")
port = os.getenv("port")
database = os.getenv("db_name")
connection_string = (
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)


def db_session() -> Session:
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(url=DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# Meant to be used with Depends() in path operations
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

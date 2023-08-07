from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(url="postgresql+psycopg2://localhost:localhost@localhost/auth")

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

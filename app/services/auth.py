from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..db.models.user import User
from ..db.setup import get_db

# Get these from env in production
SECRET_KEY = "Super Secret Key"
ALGORITHM = "HS256"
EXPIRY_MINUTES = 60


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    stmt = select(User).where(User.email == email)
    user = db.scalar(stmt)
    if user is None:
        raise credentials_exception
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)

def generate_jwt(user: User):
    data = {"sub": user.email}
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate(db: Session, username: str, password: str):
    stmt = select(User).where(User.email == username)
    user = db.scalar(stmt)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user
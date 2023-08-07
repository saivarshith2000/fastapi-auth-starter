from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..services.auth import authenticate, generate_jwt, hash_password, get_current_user

from ..db.models.user import Role, User

from ..db.setup import get_db
from ..schema.auth import SignUpSchema, UserSchema, Token

router = APIRouter(prefix="/auth")

@router.get("/me", response_model=UserSchema)
def me(user: Annotated[UserSchema, Depends(get_current_user)]):
    return user


@router.post("/signup", response_model=UserSchema)
def signup(user: SignUpSchema, db: Annotated[Session, Depends(get_db)]):
    stmt = select(User).where(User.email == user.email)
    user_in_db = db.scalar(stmt)
    if user_in_db:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    db_user = User(
        email = user.email, 
        password_hash = hash_password(user.password), 
        first_name = user.first_name, 
        last_name = user.last_name,
        role = Role.USER
        )
    db.add(db_user)
    db.commit()
    return db_user


@router.post("/signin", response_model=Token)
def signin(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user = authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = generate_jwt(user)
    return Token(access_token=token, token_type = "bearer")
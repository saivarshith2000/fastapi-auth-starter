from typing import Annotated
from fastapi import APIRouter, Depends

from ..db.models.user import User
from ..services.auth import get_current_user

router = APIRouter(prefix="/protected")

@router.get("/")
def protected_route(user: Annotated[User, Depends(get_current_user)]):
    return f"Congrats {user.first_name}, {user.last_name}! This is a protected route and you can see it !"
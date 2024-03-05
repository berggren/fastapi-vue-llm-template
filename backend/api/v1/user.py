from fastapi import APIRouter, Depends
from api.auth.google import get_current_user
from api.datastores.sql.schemas import User

router = APIRouter()


@router.get("/me", response_model=User)
def me(user: User = Depends(get_current_user)):
    return user

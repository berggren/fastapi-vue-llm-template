from pydantic import BaseModel
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import APIKeyCookie

from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from sqlalchemy.orm import Session

from jose import JWTError, jwt

from api.datastores.sql.database import get_db_connection

from api.config import config

from api.datastores.sql import models, crud
from api.datastores.sql.schemas import User


router = APIRouter()
oauth = OAuth()

cookie_scheme = APIKeyCookie(name="access_token", auto_error=False)

GOOGLE_CLIENT_ID = config["auth"]["google"]["client_id"]
GOOGLE_CLIENT_SECRET = config["auth"]["google"]["client_secret"]

oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    client_kwargs={"scope": "openid email profile"},
)

# JWT settings
SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080


class TokenData(BaseModel):
    email: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    access_token_expires = timedelta(expires_delta)
    expire = datetime.now(timezone.utc) + access_token_expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(cookie_scheme), db: Session = Depends(get_db_connection)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if not user:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/login")
async def login(request: Request):
    redirect_uri = str(request.url_for("auth"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth")
async def auth(request: Request, db: Session = Depends(get_db_connection)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f"<h1>{error.error}</h1>")
    user_info = token.get("userinfo")
    user_model = models.User(
        name=user_info.get("name", ""),
        email=user_info.get("email", ""),
        picture=user_info.get("picture", ""),
    )
    db_user = crud.get_user_by_email(db, email=user_model.email)
    if not db_user:
        db_user = crud.create_user(db, user_model)

    response = RedirectResponse(url="http://localhost:3000")

    # Create JWT access token
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    # Set the JWT cookie in the response
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return response


@router.delete("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out"}

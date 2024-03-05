from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from api.auth import google as google_auth
from api.v1 import system as system_v1, user as user_v1, prompt as prompt_v1
from api.config import config
from api.datastores.sql import models
from api.datastores.sql.database import engine


# Allow Frontend origin to make API calls.
origins = config["server"]["allowed_origins"]

# Initialize database
models.Base.metadata.create_all(bind=engine)

# Create the main app
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=config["auth"]["secret_session_key"])

# Create app for API version 1
api_v1 = FastAPI()

# Mount the API app
app.mount("/api/v1", api_v1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_v1.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(google_auth.router)

api_v1.include_router(
    user_v1.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(google_auth.get_current_active_user)],
)
api_v1.include_router(
    system_v1.router,
    prefix="/system",
    tags=["system"],
    dependencies=[Depends(google_auth.get_current_active_user)],
)
api_v1.include_router(
    prompt_v1.router,
    prefix="/prompt",
    tags=["prompt"],
    dependencies=[Depends(google_auth.get_current_active_user)],
)

from datetime import datetime, timedelta
from typing import List
from uuid import uuid4

import bcrypt
import jwt
from sqlalchemy import Column, Table
from sqlalchemy.types import String, DateTime, DECIMAL, LargeBinary
from sqlalchemy.sql import func
from fastapi import HTTPException

from api.main import database, metadata, JWT_SECRET_KEY, JWT_EXPIRATION_MINUTES
from api.models.user import User, UserIn
from api import auth


users = Table(
    "users",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("email", String(128), unique=True, nullable=False),
    Column("_password", LargeBinary(60)),
    Column("pseudonym", String(128)),
    Column("created_at", DateTime, server_default=func.datetime("now"), nullable=False),
    Column("modified_at", DateTime, server_default=func.datetime("now"), onupdate=func.datetime("now"), nullable=False)
)


async def get_user(user_id: str) -> User:
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


async def get_user_by_email(email: str) -> User:
    query = users.select().where(users.c.email == email)
    return await database.fetch_one(query)


async def list_users() -> List[User]:
    query = users.select()
    return await database.fetch_all(query)


async def create_user(user: UserIn) -> User:
    user_id: str = str(uuid4())
    query = users.insert().values(
        id=user_id,
        email=user.email,
        _password=bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()),
        pseudonym=user.pseudonym
    )
    await database.execute(query)
    return await get_user(user_id=user_id)


async def validate_user_password(email: str, password_guess: str):
    user = await get_user_by_email(email)

    if not bcrypt.checkpw(password_guess.encode(), user._password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return auth.create_jwt(user)

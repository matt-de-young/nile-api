from datetime import datetime
from typing import List
from uuid import uuid4

import bcrypt
from sqlalchemy import Column, Table
from sqlalchemy.types import String, DateTime, LargeBinary
from sqlalchemy.sql import func
from fastapi import HTTPException

from api.main import database, metadata
from api.models.user import User, UserIn


users = Table(
    "users",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("email", String(128), unique=True, nullable=False),
    Column("_password", LargeBinary(60)),
    Column("pseudonym", String(128)),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column(
        "modified_at",
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
)


async def get_user(user_id: str) -> User:
    """ Returns a User with the given id. """
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


async def get_user_by_email(email: str) -> User:
    """ Returns a User with the given email. """
    query = users.select().where(users.c.email == email)
    return await database.fetch_one(query)


async def list_users() -> List[User]:
    """ Lists Users matching the provided parameters. """
    query = users.select()
    return await database.fetch_all(query)


async def create_user(user: UserIn) -> User:
    """ Creates & returns a User. """
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
    """ Returns a User if email matches &  password guess is correct. """
    user = await get_user_by_email(email)

    if not bcrypt.checkpw(password_guess.encode(), user._password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return user

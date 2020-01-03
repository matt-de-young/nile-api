from api.models.user import UserIn
from typing import List
from uuid import uuid4

from sqlalchemy import Column, Table
from sqlalchemy.types import String, DateTime, DECIMAL, LargeBinary
from sqlalchemy.sql import func

from api.main import database, metadata
from api.models.user import User, UserIn


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


async def list_users() -> List[User]:
    query = users.select()
    return await database.fetch_all(query)


async def create_user(user: UserIn) -> User:
    user_id: str = str(uuid4())
    query = users.insert().values(
        id=user_id,
        email=user.email,
        pseudonym=user.pseudonym
    )
    await database.execute(query)
    return await get_user(user_id=user_id)

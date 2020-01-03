from typing import List
from fastapi import APIRouter

router = APIRouter()

from api.models.user import User, UserIn
from api.store import user as user_store


@router.get("/", response_model=List[User])
async def read_users():
    return await user_store.list_users()


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: str):
    return await user_store.get_user(user_id)


@router.post("/", response_model=User)
async def create_user(book: UserIn):
    return await user_store.create_user(book)

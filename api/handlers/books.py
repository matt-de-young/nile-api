from typing import List

from fastapi import APIRouter, Depends

from api.models.user import User
from api.models.book import Book, BookIn
from api.store import book as book_store
from api.auth import get_current_user


router = APIRouter()

@router.get("/", response_model=List[Book])
async def read_books(user_id: str = None):
    return await book_store.list_books(user_id)


@router.post("/", response_model=Book)
async def create_book(book: BookIn, user: User = Depends(get_current_user)):
    return await book_store.create_book(book, user=user)

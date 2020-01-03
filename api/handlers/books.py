from typing import List

from fastapi import APIRouter

from api.models.book import Book, BookIn
from api.store import book as book_store


router = APIRouter()

@router.get("/", response_model=List[Book])
async def read_books(user_id: str = None):
    return await book_store.list_books(user_id)


@router.post("/", response_model=Book)
async def create_book(book: BookIn):
    return await book_store.create_book(book)

from typing import List

from fastapi import APIRouter, Depends, HTTPException

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


@router.get("/{book_id}", response_model=Book)
async def read_book(book_id: str):
    return await book_store.get_book(book_id)


@router.delete("/{book_id}")
async def delete_book(book_id: str, user: User = Depends(get_current_user)):
    book = await book_store.get_book(book_id)
    if book.user_id != user.id:
        raise HTTPException(status_code=403, detail="Cannot delete a book belonging to another user.")
    await book_store.delete_book(book_id)

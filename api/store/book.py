from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import String, DateTime, DECIMAL
from sqlalchemy.sql import func, select, or_

from api.main import database, metadata
from api.models.book import Book, BookIn
from api.models.user import User
from api.store.user import users


books = Table(
    "books",
    metadata,
    Column("id", String(36), primary_key=True, default=str(uuid4())),
    Column("title", String(128), nullable=False),
    Column("description", String),
    Column("user_id", String(36), ForeignKey("users.id"), nullable=False),
    Column("price_in_eur", DECIMAL(9, 2)),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column(
        "modified_at",
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
)

async def get_book(book_id: str) -> Book:
    """ Returns a Book with the given id. """
    query = select([
        books,
        users.c.pseudonym.label('author')
    ]).select_from(books.join(users)).where(books.c.id == book_id)
    return await database.fetch_one(query)


async def list_books(
        user_id: str = None,
        q: str = None,
        sort_col: Optional[str] = "modified_at",
        sort_order: Optional[str] = "desc"
) -> List[Book]:
    """ Lists Books matching the provided parameters. """
    query = select([books, users.c.pseudonym.label('author')]).select_from(books.join(users))
    if user_id:
        query = query.where(books.c.user_id == user_id)
    if q:
        query = query.where(or_(
            books.c.title.ilike(f"%{q}%"),
            books.c.description.ilike(f"%{q}%")
        ))

    try:
        query = query.order_by(getattr(getattr(books.c, sort_col), sort_order)())
    except AttributeError as ex:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort parameter '{ex}'.",
        )

    return await database.fetch_all(query)


async def create_book(book: BookIn, user: User) -> Book:
    """ Creates & returns a Book. """
    book_id: str = str(uuid4())
    query = books.insert().values(
        **book.dict(),
        id=book_id,
        user_id=user.id
    )
    await database.execute(query)
    return await get_book(book_id=book_id)


async def delete_book(book_id: str) -> None:
    """ Deletes a Book with the given id. """
    query = books.delete().where(books.c.id == book_id)
    await database.fetch_one(query)

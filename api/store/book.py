from typing import List
from uuid import uuid4

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import String, DateTime, DECIMAL
from sqlalchemy.sql import func

from api.main import database, metadata
from api.models.book import Book, BookIn


books = Table(
    "books",
    metadata,
    Column("id", String(36), primary_key=True, default=str(uuid4())),
    Column("title", String(128), nullable=False),
    Column("description", String),
    Column("user_id", String(36), ForeignKey("users.id"), nullable=False),
    Column("price_in_eur", DECIMAL(9, 2)),
    Column("created_at", DateTime, server_default=func.datetime("now"), nullable=False),
    Column("modified_at", DateTime, server_default=func.datetime("now"), onupdate=func.datetime("now"), nullable=False)
)

async def get_book(book_id: str) -> Book:
    query = books.select().where(books.c.id == book_id)
    return await database.fetch_one(query)

async def list_books(user_id:str = None) -> List[Book]:
    query = books.select()
    if user_id:
        query = query.where(books.c.user_id == user_id)
    return await database.fetch_all(query)

async def create_book(book: BookIn) -> Book:
    book_id: str = str(uuid4())
    query = books.insert().values(
        **book.dict(),
        id=book_id
    )
    await database.execute(query)
    return await get_book(book_id=book_id)

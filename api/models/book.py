from typing import Optional

from datetime import datetime
from pydantic import BaseModel

class BookIn(BaseModel):
    """ Represents the user input for a new Book. """
    title: str
    description: Optional[str]
    price_in_eur: Optional[float]


class Book(BaseModel):
    """ Represents how a Book is returned to the user. """
    id: str
    title: str
    description: Optional[str]
    user_id: str
    author: Optional[str]
    price_in_eur: Optional[float]
    created_at: datetime
    modified_at: datetime

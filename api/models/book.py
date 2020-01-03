from typing import Optional

from datetime import datetime
from pydantic import BaseModel

class BookIn(BaseModel):
    title: str
    description: Optional[str]
    price_in_eur: Optional[float]


class Book(BaseModel):
    id: str
    title: str
    description: Optional[str]
    user_id: str
    author: Optional[str]
    price_in_eur: Optional[float]
    created_at: datetime
    modified_at: datetime

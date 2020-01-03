from datetime import datetime
from pydantic import BaseModel

class UserIn(BaseModel):
    email: str
    password: str
    pseudonym: str

class User(BaseModel):
    id: str
    email: str
    _password: str
    pseudonym: str
    created_at: datetime
    modified_at: datetime

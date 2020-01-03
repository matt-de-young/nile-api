from datetime import datetime
from pydantic import BaseModel

class UserIn(BaseModel):
    """ Represents the user input for a new User. """
    email: str
    password: str
    pseudonym: str

class User(BaseModel):
    """ Represents how a User is returned to the user. """
    id: str
    email: str
    _password: str
    pseudonym: str
    created_at: datetime
    modified_at: datetime

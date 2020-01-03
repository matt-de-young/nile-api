from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException

from api.main import oauth2_scheme, JWT_SECRET_KEY, JWT_EXPIRATION_MINUTES, JWT_ALGORITHM
from api.models.user import User
from api.store import user as user_store


def create_jwt(user: User) -> bytes:
    """ Creates a JWT for the User. """
    return jwt.encode(
        {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
        },
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """ Returns the user decoded from a JWT. """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = await user_store.get_user(username)
    if user is None:
        raise credentials_exception
    return user

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.store import user as user_store
from api.auth import create_jwt

router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Get a new JWT using basic auth. """
    try:
        user = await user_store.validate_user_password(
            email=form_data.username,
            password_guess=form_data.password
        )
    except Exception as ex:
        # TODO: catch real 404 & password missmatch exceptions
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": create_jwt(user), "token_type": "bearer"}

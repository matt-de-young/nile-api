from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.store import user as user_store


router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        access_token = await user_store.validate_user_password(
            email=form_data.username,
            password_guess=form_data.password
        )
    except Exception as ex:
        # TODO: catch real 404 & password missmatch exceptions
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": access_token, "token_type": "bearer"}

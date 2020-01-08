
import os

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
import databases
import sqlalchemy


DATABASE_URL = os.getenv("DATABASE_URL")
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = "4702b7871304fa054bf0487c961b27c7536fab03a4a77478a6b50a11104b92d1"
JWT_EXPIRATION_MINUTES = 15

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@app.on_event("startup")
async def startup():
    """ Runs when the server is started. """
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """ Runs when the server is stopped gracefully. """
    await database.disconnect()


from api.handlers import books, users, token

app.include_router(
    token.router,
    tags=["auth"]
)
app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)
app.include_router(
    books.router,
    prefix="/books",
    tags=["books"],
)

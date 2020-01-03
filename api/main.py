from fastapi import FastAPI
import databases
import sqlalchemy


DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


from api.handlers import books, users

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

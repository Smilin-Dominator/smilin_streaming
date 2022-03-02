from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from databases import Database as Db
from sqlalchemy import create_engine
from formats import User, Queries

app = FastAPI()
DATABASE_URL = "mysql+pymysql://root:override@localhost/app"
database = Db(DATABASE_URL)
engine = create_engine(DATABASE_URL)
queries = Queries()


@app.on_event("startup")
async def start_db():
    await database.connect()


@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()


@app.get("/users/{username}/exists")
async def exists(username: str):
    query = "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = :username;"
    result = await database.fetch_one(query, {"username": username})
    if result:
        return True
    else:
        return False

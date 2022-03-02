from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from databases import Database as Db
from sqlalchemy import create_engine
from formats import User, Queries
from string import ascii_lowercase, ascii_uppercase, hexdigits, octdigits
from random import choice
from hashlib import sha256

app = FastAPI()
DATABASE_URL = "mysql+pymysql://root:override@localhost/app"
database = Db(DATABASE_URL)
engine = create_engine(DATABASE_URL)
queries = Queries()


@app.on_event("startup")
async def start_db():
    await database.connect()
    if (not await exists("songs")) and (not await exists("app")):
        await database.execute(queries.FIRST_TIME_SETUP)


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


@app.get("/users/{username}/register")
async def register(username: str, email: str, password: str):
    if not await exists(username):
        salt1 = ''.join([choice(choice([ascii_uppercase, ascii_lowercase, hexdigits, octdigits])) for _ in range(512)])
        salt2 = ''.join([choice(choice([ascii_uppercase, ascii_lowercase, hexdigits, octdigits])) for _ in range(512)])
        hashed_pass = sha256(''.join([salt1, password, salt2]).encode('utf-8')).hexdigest()
        await database.execute(queries.USER_SETUP, {
            "username": username,
            "email": email,
            "password_hash": hashed_pass,
            "salt1": salt1,
            "salt2": salt2
        })
        return "Success!"
    else:
        return "User Already Exists!"

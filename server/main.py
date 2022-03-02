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


async def db_exists(tbl: str):
    query = "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = :db;"
    result = await database.fetch_one(query, {"db": tbl})
    return False if result is None else True


async def user_exists(username: str, email: str):
    query = "SELECT username FROM users WHERE username = :username OR email = :email"
    result = await database.fetch_one(query, {"username": username, "email": email})
    if result:
        return True
    else:
        return False


@app.on_event("startup")
async def start_db():
    await database.connect()
    if (not await db_exists("songs")) and (not await db_exists("app")):
        await database.execute(queries.FIRST_TIME_SETUP)


@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()


@app.get("/users/{username}/exists")
async def user_check(username: str, email: str):
    return user_exists(username, email)


@app.get("/users/{username}/register")
async def register(username: str, email: str, password: str):
    if not await user_exists(username, email):
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

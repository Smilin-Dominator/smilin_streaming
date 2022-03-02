from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from databases import Database as Db
from sqlalchemy import create_engine
from formats import User
from string import ascii_lowercase, ascii_uppercase, hexdigits, octdigits
from random import choice
from hashlib import sha256

app = FastAPI()
DATABASE_URL = "mysql+pymysql://root:override@localhost/app"
database = Db(DATABASE_URL)
engine = create_engine(DATABASE_URL)


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
    if (not await db_exists("songs")) or (not await db_exists("app")):
        await database.execute("""
            CREATE DATABASE IF NOT EXISTS app;
            
            CREATE TABLE IF NOT EXISTS app.users (
                username VARCHAR(50) PRIMARY KEY,
                email VARCHAR(256),
                password_hash VARCHAR(256),
                salt1 VARCHAR(512),
                salt2 VARCHAR(512)
            );
            
            CREATE DATABASE IF NOT EXISTS songs;
          
            CREATE TABLE IF NOT EXISTS songs.artists (
                id INT PRIMARY KEY,
                name VARCHAR(256)
            );
          
            CREATE TABLE IF NOT EXISTS songs.songs (
                 id INT PRIMARY KEY,
                 name VARCHAR(256),
                 genre VARCHAR(20),
                 artist_id INT,
                 FOREIGN KEY (artist_id) REFERENCES songs.artists(id)
            );        
        """)


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
        await database.execute("""
            INSERT INTO app.users (username, email, password_hash, salt1, salt2)
            VALUES (:username, :email, :password_hash, :salt1, :salt2);
        """, {
            "username": username,
            "email": email,
            "password_hash": hashed_pass,
            "salt1": salt1,
            "salt2": salt2
        })
        await database.execute(f"""

            CREATE DATABASE `{username}`;
            USE `{username}`;
            
            CREATE TABLE song_history (
                song_id INT PRIMARY KEY,
                listen_count INT,
                FOREIGN KEY (song_id) REFERENCES songs.songs(id)
            );
            
            CREATE TABLE artist_history (
                artist_id INT PRIMARY KEY,
                listen_count INT,
                FOREIGN KEY (artist_id) REFERENCES songs.artists(id)
            );
            
        """)
        return "Success!"
    else:
        return "User Already Exists!"

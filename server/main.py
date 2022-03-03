from fastapi import FastAPI, Depends
from pathlib import Path
from databases import Database as Db
from sqlalchemy import create_engine
from formats import User
from string import ascii_lowercase, ascii_uppercase, hexdigits, octdigits
from random import choice
from hashlib import sha256
from datetime import datetime

app = FastAPI()
DATABASE_URL = "mysql+pymysql://root:override@localhost/app"
database = Db(DATABASE_URL)
engine = create_engine(DATABASE_URL)
songs = Path("songs")


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
    songs.mkdir() if not songs.exists() else None
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


@app.get("/users/exists")
async def user_check(username: str, email: str):
    return await user_exists(username, email)


@app.post("/users/login")
async def login(password: str, username: str):
    hash, salt1, salt2, email = await database.fetch_one(
        "SELECT password_hash, salt1, salt2, email FROM users WHERE username = :username;", {"username": username}
    )
    new_hash = sha256(''.join([salt1, password, salt2]).encode('utf-8')).hexdigest()
    if new_hash == hash:
        return User(username=username, email=email, password_hash=hash)
    else:
        return False


@app.post("/users/register")
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
            
            CREATE TABLE playlists (
                name VARCHAR(250) PRIMARY KEY,
                table_name VARCHAR(256)
            )
            
            USE app;
            
        """)
        return "Success!"
    else:
        return "User Already Exists!"


@app.get("/playlists/list")
async def list_playlists(user: User = Depends(login)):
    return await database.fetch_all(f"SELECT name FROM {user.username}.playlists")


@app.post("/playlists/create")
async def create_playlist(name: str, user: User = Depends(login)):
    exists = await database.fetch_one(f"SELECT name FROM {user.username}.playlists WHERE name = :name", {
        "name": name
    })
    if not exists:
        table = "playlist_" + name.lower().replace(" ", "_")
        await database.execute(f"INSERT INTO {user.username}.playlists VALUES (:name, :table_name)", {
            "name": name,
            "table_name": table
        })
        await database.execute(f"""
            CREATE TABLE {user.username}.{table} (
                song_id INT PRIMARY KEY,
                date_added DATE,
                FOREIGN KEY (song_id) REFERENCES songs.songs(id)
            )
        """)
        return True
    else:
        return False


@app.get("/playlists/get")
async def describe_playlist(name: str, user: User = Depends(login)):
    table_name = await database.fetch_one(f"SELECT table_name FROM {user.username}.playlists WHERE name = :name", {
        "name": name
    })
    return await database.fetch_all(f"""
        SELECT 
            songs.songs.name AS name,
            songs.artists.name AS artist,
            date_added AS date 
        FROM {user.username}.{table_name[0]} 
            INNER JOIN songs.songs ON songs.songs.id = song_id
            INNER JOIN songs.artists ON songs.songs.id = songs.artists.id;
    """)


@app.post("/playlists/delete")
async def drop_playlist(name: str, user: User = Depends(login)):
    table_name = await database.fetch_one(f"SELECT table_name FROM {user.username}.playlists WHERE name = :name", {
        "name": name
    })
    if not table_name:
        return False
    await database.execute(f"DROP TABLE {user.username}.{table_name[0]};")
    await database.execute(f"DELETE FROM {user.username}.playlists WHERE name = {name};")
    return True


@app.post("/playlists/songs/add")
async def add_song(name: str, song: str, user: User = Depends(login)):
    playlist_table = await database.fetch_one(f"SELECT table_name FROM {user.username}.playlists WHERE name = :name", {
        "name": name
    })
    song_id = await database.fetch_one(f"SELECT id FROM songs.songs WHERE songs.name = :song", {
        "song": song
    })
    exists = await database.fetch_one(f"SELECT song_id FROM {user.username}.{playlist_table[0]} WHERE song_id = :id", {
        "id": song_id[0]
    })
    if (not song_id) or (not playlist_table) or exists:
        return False
    await database.execute(f"INSERT INTO {user.username}.{playlist_table[0]} VALUES (:sid, :date)", {
        "sid": song_id[0],
        "date": datetime.now()
    })
    return True


@app.post("/playlists/songs/delete")
async def remove_song(name: str, song: str, user: User = Depends(login)):
    playlist_table = await database.fetch_one(f"SELECT table_name FROM {user.username}.playlists WHERE name = :name", {
        "name": name
    })
    song_id = await database.fetch_one(f"SELECT id FROM songs.songs WHERE songs.name = :song", {
        "song": song
    })
    if (not song_id) or (not playlist_table):
        return False
    await database.execute(f"DELETE FROM {user.username}.{playlist_table[0]} WHERE song_id = :id", {
        "id": song_id[0]
    })
    return True

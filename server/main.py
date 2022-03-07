from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.responses import FileResponse
from pathlib import Path
from databases import Database as Db
from sqlalchemy import create_engine
from formats import User, Artist
from string import ascii_lowercase, ascii_uppercase, hexdigits, octdigits
from random import choice
from hashlib import sha256
from datetime import datetime
from shutil import copyfileobj

app = FastAPI()
DATABASE_URL = "mysql+pymysql://root:override@localhost/app"
database = Db(DATABASE_URL)
engine = create_engine(DATABASE_URL)
songs = Path("songs")


async def db_exists(tbl: str):
    query = "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = :db;"
    result = await database.fetch_one(query, {"db": tbl})
    return False if result is None else True


async def user_exists(username: str):
    query = "SELECT username FROM users WHERE username = :username"
    result = await database.fetch_one(query, {"username": username})
    if result:
        return True
    else:
        return False


async def artist_exists(username: str):
    result = await database.fetch_one("SELECT username FROM artists WHERE username = :username", {
        "username": username
    })
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
                password_hash VARCHAR(256),
                salt1 VARCHAR(512),
                salt2 VARCHAR(512)
            );
            
            CREATE TABLE IF NOT EXISTS app.artists (
                name VARCHAR(256) PRIMARY KEY,
                username VARCHAR(50),
                password_hash VARCHAR(256),
                salt1 VARCHAR(512),
                salt2 VARCHAR(512)
            );
            
            CREATE DATABASE IF NOT EXISTS songs;
          
            CREATE TABLE IF NOT EXISTS songs.artists (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(256),
                followers INT,
                FOREIGN KEY (name) REFERENCES app.artists(name)
            );
          
            CREATE TABLE IF NOT EXISTS songs.songs (
                 id INT PRIMARY KEY AUTO_INCREMENT,
                 name VARCHAR(256),
                 artist_id INT,
                 album VARCHAR(256),
                 genre VARCHAR(20),
                 filename VARCHAR(256),
                 listen_count INT,
                 FOREIGN KEY (artist_id) REFERENCES songs.artists(id)
            );        
        """)


@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()


@app.get("/users/exists")
async def user_check(username: str):
    return await user_exists(username)


@app.get("/artists/exists")
async def artist_check(username: str):
    return await artist_exists(username)


@app.post("/users/login")
async def user_login(password: str, username: str):
    try:
        hash, salt1, salt2 = await database.fetch_one(
            "SELECT password_hash, salt1, salt2 FROM users WHERE username = :username;", {"username": username}
        )
        new_hash = sha256(''.join([salt1, password, salt2]).encode('utf-8')).hexdigest()
        if new_hash == hash:
            return User(username=username, password_hash=hash)
        else:
            return False
    except TypeError:
        return False


@app.post("/artists/login")
async def artist_login(password: str, username: str):
    hash, salt1, salt2, name = await database.fetch_one(
        "SELECT password_hash, salt1, salt2, name FROM artists WHERE username = :username;", {"username": username}
    )
    new_hash = sha256(''.join([salt1, password, salt2]).encode('utf-8')).hexdigest()
    if new_hash == hash:
        id = await database.fetch_one("SELECT id FROM songs.artists WHERE name = :name", {"name": name})
        return Artist(id=id[0], name=name, username=username, password_hash=new_hash)
    else:
        return False


@app.post("/users/register")
async def register(username: str, password: str):
    if not await user_exists(username):
        salt1 = ''.join([choice(choice([ascii_uppercase, ascii_lowercase, hexdigits, octdigits])) for _ in range(512)])
        salt2 = ''.join([choice(choice([ascii_uppercase, ascii_lowercase, hexdigits, octdigits])) for _ in range(512)])
        hashed_pass = sha256(''.join([salt1, password, salt2]).encode('utf-8')).hexdigest()
        await database.execute("""
            INSERT INTO app.users (username, password_hash, salt1, salt2)
            VALUES (:username, :password_hash, :salt1, :salt2);
        """, {
            "username": username,
            "password_hash": hashed_pass,
            "salt1": salt1,
            "salt2": salt2
        })
        await database.execute(f"""

            CREATE DATABASE {username};
            
            CREATE TABLE {username}.song_history (
                song_id INT PRIMARY KEY,
                listen_count INT,
                FOREIGN KEY (song_id) REFERENCES songs.songs(id)
            );
            
            CREATE TABLE {username}.artist_history (
                artist_id INT PRIMARY KEY,
                listen_count INT,
                FOREIGN KEY (artist_id) REFERENCES songs.artists(id)
            );
            
            CREATE TABLE {username}.playlists (
                name VARCHAR(250) PRIMARY KEY,
                table_name VARCHAR(256)
            )
            
            CREATE TABLE {username}.following (
                artist_id INT PRIMARY KEY,
                FOREIGN KEY (artist_id) REFERENCES songs.artists(id)
            )
                        
        """)
        return "Success!"
    else:
        return "User Already Exists!"


@app.post("/artists/register")
async def register_artist(name: str, username: str, password: str):
    if not await artist_exists(username):
        salt1 = ''.join([choice(choice([ascii_uppercase, ascii_lowercase, hexdigits, octdigits])) for _ in range(512)])
        salt2 = ''.join([choice(choice([ascii_uppercase, ascii_lowercase, hexdigits, octdigits])) for _ in range(512)])
        hashed_pass = sha256(''.join([salt1, password, salt2]).encode('utf-8')).hexdigest()
        await database.execute("""
            INSERT INTO app.artists (name, username, password_hash, salt1, salt2)
            VALUES (:name, :username, :password_hash, :salt1, :salt2);
        """, {
            "name": name,
            "username": username,
            "password_hash": hashed_pass,
            "salt1": salt1,
            "salt2": salt2
        })
        await database.execute(f"INSERT INTO songs.artists(name, followers) VALUES (:name, 0)", {
            "name": name
        })
        return True
    else:
        return "Artist Already Exists!"


@app.get("/playlists/list")
async def list_playlists(user: User = Depends(user_login)):
    return await database.fetch_all(f"SELECT name FROM {user.username}.playlists")


@app.post("/playlists/create")
async def create_playlist(name: str, user: User = Depends(user_login)):
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
async def describe_playlist(name: str, user: User = Depends(user_login)):
    table_name = await database.fetch_one(f"SELECT table_name FROM {user.username}.playlists WHERE name = :name", {
        "name": name
    })
    return await database.fetch_all(f"""
        SELECT 
            songs.songs.name AS name,
            songs.artists.name AS artist,
            songs.songs.album AS album,
            date_added AS date 
        FROM {user.username}.{table_name[0]} 
            INNER JOIN songs.songs ON songs.songs.id = song_id
            INNER JOIN songs.artists ON songs.artists.id = songs.songs.artist_id;
    """)


@app.post("/playlists/delete")
async def drop_playlist(name: str, user: User = Depends(user_login)):
    table_name = await database.fetch_one(f"SELECT table_name FROM {user.username}.playlists WHERE name = :name", {
        "name": name
    })
    if not table_name:
        return False
    await database.execute(f"DROP TABLE {user.username}.{table_name[0]};")
    await database.execute(f"DELETE FROM {user.username}.playlists WHERE name = :name;", {
        "name": name
    })
    return True


@app.post("/playlists/songs/add")
async def add_song(name: str, song: str, user: User = Depends(user_login)):
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
async def remove_song(name: str, song: str, user: User = Depends(user_login)):
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


@app.get("/songs/listen")
async def listen(song: str, user: User = Depends(user_login)):

    async def update_song_history():
        listen_count = await database.fetch_one(f"SELECT listen_count FROM {user.username}.song_history WHERE song_id = :id", {
            "id": song_id
        })
        if listen_count is None:
            await database.execute(f"INSERT INTO {user.username}.song_history VALUES (:sid, 1)", {
                "sid": song_id
            })
        else:
            await database.execute(f"UPDATE {user.username}.song_history SET listen_count = listen_count + 1 WHERE song_id = :sid", {
                "sid": song_id
            })
        await database.execute(f"UPDATE songs.songs SET listen_count = listen_count + 1 WHERE id = :id", {
            "id": song_id
        })

    async def update_artist_history():
        listen_count = await database.fetch_one(f"SELECT listen_count FROM {user.username}.artist_history WHERE artist_id = :id", {
            "id": artist_id
        })
        if listen_count is None:
            await database.execute(f"INSERT INTO {user.username}.artist_history VALUES (:aid, 1)", {
                "aid": artist_id
            })
        else:
            await database.execute(f"UPDATE {user.username}.artist_history SET listen_count = :lc WHERE artist_id = :aid", {
                "lc": listen_count[0] + 1,
                "aid": artist_id
            })

    song_id, filename, artist_id = await database.fetch_one(f"SELECT id, filename, artist_id FROM songs.songs WHERE songs.name = :song", {
        "song": song
    })
    if filename is None:
        return False
    else:
        await update_song_history()
        await update_artist_history()
        return FileResponse(path=filename)


@app.post("/songs/upload")
async def upload_song(song_name: str, album: str, genre: str, filename: str, song: UploadFile = File(...), artist: Artist = Depends(artist_login)):
    path = Path("songs").joinpath(filename)
    with open(path, "wb") as w:
        copyfileobj(song.file, w)
    await database.execute(
        "INSERT INTO songs.songs(name, artist_id, album, genre, filename, listen_count) VALUES(:name, :aid, :album, :genre, :filename, :listen_count)", {
          "name": song_name,
          "aid": artist.id,
          "album": album,
          "genre": genre,
          "filename": str(path),
          "listen_count": 0
        })
    return True


@app.get("/songs/recommend/previous")
async def recommend_previous(user: User = Depends(user_login)):
    out = await database.fetch_all(f"""
        SELECT songs.songs.name AS name,
            songs.artists.name AS artist, 
            songs.songs.album AS album
        FROM {user.username}.song_history
            INNER JOIN songs.songs ON songs.songs.id = song_id
            INNER JOIN songs.artists ON songs.artists.id = songs.songs.artist_id
         ORDER BY {user.username}.song_history.listen_count
         LIMIT 5
    """)
    if not out:
        return False
    else:
        return out


@app.get("/songs/recommend/artists")
async def recommended_from_artists(user: User = Depends(user_login)):
    artists = await database.fetch_all(f"""
        SELECT {user.username}.following.artist_id, {user.username}.artist_history.listen_count 
        FROM {user.username}.following 
        INNER JOIN {user.username}.artist_history ON {user.username}.artist_history.artist_id = {user.username}.following.artist_id
        ORDER BY listen_count 
        LIMIT 3;
    """)
    if not artists:
        return False
    else:
        out = []
        query = f"""
            SELECT songs.songs.name AS name,
                songs.artists.name AS artist, 
                songs.songs.album AS album
            FROM songs.songs
            INNER JOIN songs.artists ON songs.artists.id = artist_id
            WHERE artist_id = :id
             ORDER BY songs.songs.listen_count
             LIMIT 2 
        """
        for aid in artists[0]:
            out.append(await database.fetch_all(query, {"id": aid}))
        return out[0]


@app.get("/songs/get")
async def get_song(name: str, user: User = Depends(user_login)):
    result = await database.fetch_one(f"""
        SELECT songs.songs.name AS name,
            songs.artists.name AS artist, 
            songs.songs.album AS album,
            songs.songs.genre AS genre,
            songs.songs.listen_count AS listen_count
        FROM {user.username}.song_history
            INNER JOIN songs.songs ON songs.songs.id = song_id
            INNER JOIN songs.artists ON songs.artists.id = songs.songs.artist_id
        WHERE songs.name = :name;
     """, {"name": name})
    if not result:
        return False
    else:
        return result


@app.get("/artists/get")
async def get_artist(name: str, user: User = Depends(user_login)):
    id = (await database.fetch_one(f"SELECT id FROM songs.artists WHERE name = '{name}'"))[0]
    following = await database.fetch_one(f"SELECT artist_id AS following FROM {user.username}.following WHERE artist_id = {id};")
    return [
        await database.fetch_all(f"""
            SELECT artists.name AS name,
                artists.followers AS followers
            FROM songs.artists
            WHERE id = {id};
        """),
        await database.fetch_all(f"""
            SELECT DISTINCT album AS album FROM songs.songs WHERE artist_id = {id};
        """),
        await database.fetch_all(f"""
            SELECT name, listen_count, album, genre FROM songs.songs AS top_songs WHERE artist_id = {id} ORDER BY listen_count LIMIT 5;
        """),
        await database.fetch_one(f"SELECT SUM(listen_count) AS total_listens FROM songs.songs WHERE artist_id = {id}"),
        True if following else False
    ]


@app.get("/autocomplete")
async def return_results(query: str):
    ops = []
    ops.append(await database.fetch_all(f"""
        SELECT name AS song FROM songs.songs WHERE name LIKE '%{query}%';
    """))
    ops.append(await database.fetch_all(f"""
        SELECT name AS artist FROM songs.artists WHERE name LIKE '%{query}%';
    """))
    ops.append(await database.fetch_all(f"""
        SELECT DISTINCT album AS album FROM songs.songs WHERE songs.album LIKE '%{query}%';
    """))
    return ops


@app.post("/users/toggle_follow")
async def toggle_follow(name: str, user: User = Depends(user_login)):
    id: int = (await database.fetch_one(f"SELECT id FROM songs.artists WHERE name = '{name}'"))[0]
    exists = await database.fetch_one(f"SELECT artist_id AS following FROM {user.username}.following WHERE artist_id = {id};")
    if exists:
        await database.execute(f"DELETE FROM {user.username}.following WHERE artist_id = {id};")
    else:
        await database.execute(f"INSERT INTO {user.username}.following VALUES ({id});")
    return True

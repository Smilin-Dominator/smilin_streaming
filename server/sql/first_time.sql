CREATE DATABASE IF NOT EXISTS app;
CREATE TABLE app.users (
    username VARCHAR(50) PRIMARY KEY,
    email VARCHAR(256),
    password_hash VARCHAR(256),
    salt1 VARCHAR(512),
    salt2 VARCHAR(512)
);

CREATE DATABASE songs;
CREATE TABLE songs.artists (
    id INT PRIMARY KEY,
    name VARCHAR(256)
);
CREATE TABLE songs.songs (
     id INT PRIMARY KEY,
     name VARCHAR(256),
     genre VARCHAR(20),
     artist_id INT,
     FOREIGN KEY (artist_id) REFERENCES songs.artists(id)
);
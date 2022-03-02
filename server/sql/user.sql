USE app;
INSERT INTO users (username, email, password_hash, salt1, salt2)
VALUES (:username, :email, :password_hash, :salt1, :salt2);

CREATE DATABASE :username;
USE :username;
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
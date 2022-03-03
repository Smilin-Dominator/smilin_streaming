# System Database (app)

### users

| Field Name    | Data Type                |
|---------------|--------------------------|
| username      | varchar(50), primary_key |
| password_hash | varchar(256)             |
| salt1         | varchar(512)             |
| salt2         | varchar(512)             |

# Database For Each User (x)

### playlists

| Field Name | Data Type                |
|------------|--------------------------|
| name       | varchar(50), primary_key |
| table_name | varchar(256)             |


### song_history

| Field Name   | Data Type                              |
|--------------|----------------------------------------|
| song_id      | int, foreign_key (ref. songs.songs.id) |
| listen_count | int                                    |

### artist_history

| Field Name   | Data Type                                |
|--------------|------------------------------------------|
| artist_id    | int, foreign_key (ref. songs.artists.id) |
| listen_count | int                                      |

### playlist_x

| Field Name | Data Type                                             |
|------------|-------------------------------------------------------|
| song_id    | int, primary_key, foreign_key (ref. songs.artists.id) |
| date_added | datetime                                              |

# Song Database (songs)

### artists

| Field Name | Data Type        |
|------------|------------------|
| id         | int, primary_key |
| name       | varchar(256)     |

### songs

| Field Name | Data Type                                |
|------------|------------------------------------------|
| id         | int, primary_key                         |
| name       | varchar(128)                             |
| artist_id  | int, foreign_key (ref. songs.artists.id) |
| album      | varchar(256)                             |
| genre      | varchar(20)                              |
| filename   | varchar(256)                             |


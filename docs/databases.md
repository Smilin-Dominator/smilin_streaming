# System Database (app)

### users

| Field Name    | Data Type                |
|---------------|--------------------------|
| username      | varchar(50), primary_key |
| email         | varchar(256)             |
| password_hash | varchar(256)             |
| salt1         | varchar(512)             |
| salt2         | varchar(512)             |

# Database For Each User (x)

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
| genre      | varchar(20)                              |
| artist_id  | int, foreign_key (ref. songs.artists.id) |


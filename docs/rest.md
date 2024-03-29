# API Routes

## /users<hr>

#### /users/exists

| Field       | Values                                                                                        |
|-------------|-----------------------------------------------------------------------------------------------|
| Parameters  | username (string)                                                                             |
| Description | This returns 'false' if a user with the provided username doesn't exist and 'true' if it does |

#### /users/register

| Field       | Values                                                                                          |
|-------------|-------------------------------------------------------------------------------------------------|
| Parameters  | username (string), password (string)                                                            |
| Description | This checks if a user with the given username doesn't exist, and if it doesn't creates the user |

#### /users/login

| Field       | Values                                                |
|-------------|-------------------------------------------------------|
| Parameters  | username (string), password (string)                  |
| Description | This returns a User Object if the password is correct |

#### /users/toggle_follow

| Field       | Values                                                                                  |
|-------------|-----------------------------------------------------------------------------------------|
| Parameters  | name (string), username (string), password (string)                                     |
| Description | This checks if the user is following the artist, if yes it unfollows, if no, it follows |


## /artists<hr>

#### /artists/exists

| Field       | Values                                                                                           |
|-------------|--------------------------------------------------------------------------------------------------|
| Parameters  | username (string)                                                                                |
| Description | This returns 'false' if an artist with the provided username doesn't exist and 'true' if it does |

#### /artists/register

| Field       | Values                                                                                                |
|-------------|-------------------------------------------------------------------------------------------------------|
| Parameters  | username (string), password (string)                                                                  |
| Description | This checks if an artists with the given username doesn't exist, and if it doesn't creates the artist |

#### /artists/login

| Field       | Values                                                   |
|-------------|----------------------------------------------------------|
| Parameters  | username (string), password (string)                     |
| Description | This returns an Artist Object if the password is correct |

#### /artists/get/artist

| Field       | Values                                                   |
|-------------|----------------------------------------------------------|
| Parameters  | name (string), artist (Artist)                           |
| Description | This describes the artist using the artists' credentials |

#### /artists/get/user

| Field       | Values                     |
|-------------|----------------------------|
| Parameters  | name (string), user (User) |
| Description | This describes the artist  |

## /playlists<hr>

#### /playlists/list

| Field       | Values                                          |
|-------------|-------------------------------------------------|
| Parameters  | user (User)                                     |
| Description | This returns a list of all the user's playlists |

#### /playlists/create

| Field       | Values                                                         |
|-------------|----------------------------------------------------------------|
| Parameters  | name (string), user (User)                                     |
| Description | This creates a playlist, if one of the same name doesn't exist |

#### /playlists/get

| Field       | Values                       |
|-------------|------------------------------|
| Parameters  | name (string), user (User)   |
| Description | This returns a list of songs |

#### /playlists/delete

| Field       | Values                         |
|-------------|--------------------------------|
| Parameters  | name (string), user (User)     |
| Description | This deletes a user's playlist |

## /playlists/songs

#### /playlists/songs/add

| Field       | Values                                                         |
|-------------|----------------------------------------------------------------|
| Parameters  | name (string), song (string), user (User)                      |
| Description | This adds a song to the specified playlist if it doesn't exist |

#### /playlists/songs/delete

| Field       | Values                                                       |
|-------------|--------------------------------------------------------------|
| Parameters  | name (string), song (string), user (User)                    |
| Description | This deletes a song from the specified playlist if it exists |

## /songs<hr>

#### /songs/listen

| Field       | Values                     |
|-------------|----------------------------|
| Parameters  | song (string), user (User) |
| Description | This returns the song file |

#### /songs/get

| Field       | Values                     |
|-------------|----------------------------|
| Parameters  | name (string), user (User) |
| Description | This describes the song    |

#### /songs/upload

| Field       | Values                                                                                              |
|-------------|-----------------------------------------------------------------------------------------------------|
| Parameters  | song_name (string), album (string), genre (string), filename (string), song (File), artist (Artist) |
| Description | This deletes a song from the specified playlist if it exists                                        |

#### /songs/recommend/previous

| Field       | Values                                                                             |
|-------------|------------------------------------------------------------------------------------|
| Parameters  | user (User)                                                                        |
| Description | This returns a list of songs the user has listened to, ordered by the listen count |

#### /songs/recommend/artists

| Field       | Values                                                       |
|-------------|--------------------------------------------------------------|
| Parameters  | user (User)                                                  |
| Description | This returns a list of songs from 3 artists the user follows |


## /albums/get
| Field       | Values                     |
|-------------|----------------------------|
| Parameters  | name (string), user (User) |
| Description | This describes the album   |

## /autocomplete

| Field       | Values                                                    |
|-------------|-----------------------------------------------------------|
| Parameters  | query (string)                                            |
| Description | This returns a list of possible matches from the database |


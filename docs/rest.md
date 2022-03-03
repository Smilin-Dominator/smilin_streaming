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
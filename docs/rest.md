# API Routes

## /users<hr>

#### /users/exists

| Field       | Values                                                                                        |
|-------------|-----------------------------------------------------------------------------------------------|
| Parameters  | username (string), email (string)                                                             |
| Description | This returns 'false' if a user with the email or username doesn't exist and 'true' if it does |

#### /users/register

| Field       | Values                                                                                                   |
|-------------|----------------------------------------------------------------------------------------------------------|
| Parameters  | username (string), email (string), password (string)                                                     |
| Description | This checks if a user with the given email or username doesn't exist, and if it doesn't creates the user |

#### /users/login

| Field       | Values                                                |
|-------------|-------------------------------------------------------|
| Parameters  | username (string), password (string)                  |
| Description | This returns a User Object if the password is correct |


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
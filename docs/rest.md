# API Routes

## /users<hr>

#### /users/{username}/exists

| Field       | Values                                                                                        |
|-------------|-----------------------------------------------------------------------------------------------|
| Parameters  | username (string), email (string)                                                             |
| Description | This returns 'false' if a user with the email or username doesn't exist and 'true' if it does |

#### /users/{username}/register

| Field       | Values                                                                                                   |
|-------------|----------------------------------------------------------------------------------------------------------|
| Parameters  | username (string), email (string), password (string)                                                     |
| Description | This checks if a user with the given email or username doesn't exist, and if it doesn't creates the user |

#### /users/{username}/login

| Field       | Values                                                |
|-------------|-------------------------------------------------------|
| Parameters  | username (string), password (string)                  |
| Description | This returns a User Object if the password is correct |
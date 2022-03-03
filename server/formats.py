from pydantic import BaseModel


class User(BaseModel):
    username:       str
    password_hash:  str


class Artist(BaseModel):
    id:             int
    name:           str
    username:       str
    password_hash:  str

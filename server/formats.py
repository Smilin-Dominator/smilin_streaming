from pydantic import BaseModel
from dataclasses import dataclass


def read_query(fn: str):
    return open(f"sql/{fn}.sql", "r").read()


@dataclass
class Queries:
    FIRST_TIME_SETUP = read_query("first_time")
    USER_SETUP = read_query("user")


class User(BaseModel):
    username:       str
    email:          str
    password_hash:  str

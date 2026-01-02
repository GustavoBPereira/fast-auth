from pydantic import BaseModel
from datetime import datetime


class UserSchema(BaseModel):
    username: str
    password: str

class UserPublic(BaseModel):
    id: int
    username: str
    created_at: datetime


class UserList(BaseModel):
    users: list[UserPublic]
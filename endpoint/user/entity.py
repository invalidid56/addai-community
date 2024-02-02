from pydantic import BaseModel


class User(BaseModel):
    email: str
    username: str

    class Config:
        orm_mode = True


class UserCreate(User):
    password1: str
    password2: str


class UserGet(User):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

from pydantic import BaseModel
from enum import Enum


class Category(str, Enum):
    running: str = "running"
    hiking: str = "hiking"


class Article(BaseModel):
    category: Category
    title: str
    content: str

    class Config:
        orm_mode = True


class ArticleCreate(Article):
    title: str = "Title"
    content: str = "Content"


class ArticleGet(Article):
    id: int
    creator_id: int
    banner_link: str | None

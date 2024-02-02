from pydantic import BaseModel
from enum import Enum


class Category(str, Enum):
    running: str = "running"
    hiking: str = "hiking"


class Article(BaseModel):
    category: Category
    title: str
    content: str
    banner_image: str = "https://via.placeholder.com/150"

    class Config:
        orm_mode = True


class ArticleCreate(Article):
    title: str = "Title"
    content: str = "Content"


class ArticleGet(Article):
    id: int
    banner_image: str
    creator_id: int

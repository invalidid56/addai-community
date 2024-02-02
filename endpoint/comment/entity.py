from pydantic import BaseModel


class Comment(BaseModel):
    content: str

    class Config:
        orm_mode = True


class CommentCreate(Comment):
    content: str = "Content"


class CommentGet(Comment):
    id: int
    creator_id: int
    article_id: int


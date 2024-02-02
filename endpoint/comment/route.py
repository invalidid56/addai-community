from fastapi import APIRouter, Depends, status
from endpoint.user.service import (
    get_current_user,
)
import endpoint.comment.service as service
from endpoint.comment.entity import CommentGet, CommentCreate
from data.db.models import Article, User, Comment

router = APIRouter(prefix="/comment")


@router.get("/{comment_id}", response_model=CommentGet, tags=["Comment"])
async def read_comment(comment_id: int) -> Comment:
    """
    """
    return await service.get_comment(comment_id)


@router.get("/article/{article_id}", response_model=list[CommentGet], tags=["Comment"])
async def read_comments_by_article(article_id: int) -> list[Comment]:
    """
    """
    res = await service.get_comments_by_article(article_id)
    if res is None:
        return []
    return res


@router.post("/{article_id}", response_model=CommentCreate, tags=["Comment"])
async def create_comment(comment: CommentCreate, user: User = Depends(get_current_user)) -> Comment:
    """
    """
    return await service.create_comment(dict(**comment.dict(), creator_id=user.id))


@router.delete("/{comment_id}", tags=["Comment"])
async def delete_comment(comment_id: int, user: User = Depends(get_current_user)) -> None:
    """
    """
    await service.delete_comment(comment_id, user.id)

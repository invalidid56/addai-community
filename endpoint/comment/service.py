from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

import endpoint.comment.repository as repo
from data.db.models import Article, Comment


async def get_comment(comment_id: int) -> Comment:
    try:
        res = await repo.get_comment(comment_id)
    except NoResultFound:
        raise HTTPException(status_code=400, detail="Comment Not Found.")
    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23503:
            raise HTTPException(status_code=400, detail="Comment ID Not Found.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e
    return res


async def get_comments_by_article(article_id: int) -> list[Comment]:
    try:
        res = await repo.get_comments_by_article(article_id)
        if res is None:
            return []
    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23503:
            raise HTTPException(status_code=400, detail="Article Not Found.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e
    return res


async def create_comment(comment_req: dict) -> Comment:
    try:
        res: Comment = await repo.create_comment(comment_req)
    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23503:
            raise HTTPException(status_code=400, detail="Article ID Not Found.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e
    return res


async def delete_comment(comment_id: int, user_id: int) -> None:
    res = await get_comment(comment_id)
    if res.creator_id != user_id:
        raise HTTPException(status_code=403, detail="Permission Denied.")

    try:
        await repo.delete_comment(comment_id)
    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23503:
            raise HTTPException(status_code=400, detail="Comment Not Found.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e
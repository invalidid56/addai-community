from data.db.database import Transactional
from data.db.models import Comment, Article
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, insert


@Transactional()
async def get_comment(comment_id: int, session: AsyncSession = None) -> Comment:
    stmt = select(Comment).where(Comment.id == comment_id)
    result = await session.execute(stmt)
    return result.scalar_one()


@Transactional()
async def get_comments_by_article(article_id: int, session: AsyncSession = None) -> list[Comment]:
    stmt = select(Comment).where(Comment.article_id == article_id)
    result = await session.execute(stmt)
    return result.scalars().all()


@Transactional()
async def create_comment(comment: dict, session: AsyncSession = None) -> Comment:
    _comment = Comment(**comment)
    session.add(_comment)
    await session.commit()
    await session.refresh(_comment)
    return _comment


@Transactional()
async def delete_comment(comment_id: int, session: AsyncSession = None) -> None:
    await session.execute(delete(Comment).where(Comment.id == comment_id))
    await session.commit()
    return None

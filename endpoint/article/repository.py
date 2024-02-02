from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, insert
from data.db.database import Transactional
from data.db.models import Article, Banner


@Transactional()
async def get_article(article_id: int, session: AsyncSession = None) -> Article:
    result = await session.execute(select(Article).where(Article.id == article_id))
    return result.scalar_one()


@Transactional()
async def get_articles_by_category(category: str, session: AsyncSession = None) -> list[Article]:
    result = await session.execute(select(Article).where(Article.category == category))
    return result.scalars().all()


@Transactional()
async def get_articles_all(session: AsyncSession = None) -> list[Article]:
    result = await session.execute(select(Article))
    return result.scalars().all()


@Transactional()
async def create_article(article: dict, session: AsyncSession = None) -> Article:
    _article = Article(**article)

    session.add(_article)

    await session.commit()
    await session.refresh(_article)

    return _article


@Transactional()
async def update_article(article_id: int, article: dict, session: AsyncSession = None) -> None:
    await session.execute(update(Article).where(Article.id == article_id).values(article))


@Transactional()
async def delete_article(article_id: int, session: AsyncSession = None) -> None:
    await session.execute(delete(Article).where(Article.id == article_id))


@Transactional()
async def get_banner_by_article(article_id: int, session: AsyncSession = None) -> Banner:
    result = await session.execute(select(Banner).where(Banner.article_id == article_id))
    return result.scalars().all()


@Transactional()
async def create_banner(banner: dict, session: AsyncSession = None) -> Banner:
    _banner = Banner(**banner)
    session.add(_banner)
    await session.commit()
    await session.refresh(_banner)
    return _banner


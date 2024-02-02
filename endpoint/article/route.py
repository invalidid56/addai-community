from fastapi import APIRouter, Depends, status
from endpoint.user.service import (
    get_current_user,
)
import endpoint.article.service as service
from endpoint.article.entity import ArticleGet, ArticleCreate
from data.db.models import Article, User

router = APIRouter(prefix="/article")


@router.get("/", response_model=list[ArticleGet], tags=["Article"])
async def read_articles() -> list[Article]:
    """
    """
    res = await service.get_articles_all()
    if res is None:
        return []
    return res


@router.get("/{article_id}", response_model=ArticleGet, tags=["Article"])
async def read_article(article_id: int) -> Article:
    """
    """
    return await service.get_article(article_id)


@router.get("/category/{category}", response_model=list[ArticleGet], tags=["Article"])
async def read_articles_by_category(category: str) -> list[Article]:
    """
    """
    res = await service.get_articles_by_category(category)
    if res is None:
        return []
    return res


@router.post("/", response_model=ArticleCreate, tags=["Article"])
async def create_article(article: ArticleCreate, user: User = Depends(get_current_user)) -> Article:
    """
    """
    return await service.create_article(dict(**article.dict(), creator_id=user.id))


@router.put("/{article_id}", response_model=ArticleCreate, tags=["Article"])
async def update_article(article_id: int, article: ArticleCreate, user: User = Depends(get_current_user)) -> None:
    """
    """
    await service.update_article(article_id=article_id,
                                 article=article.dict(),
                                 user_id=user.id)


@router.delete("/{article_id}", tags=["Article"])
async def delete_article(article_id: int, user: User = Depends(get_current_user)) -> None:
    """
    """
    await service.delete_article(article_id, user.id)

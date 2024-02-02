from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

import endpoint.article.repository as repo
from data.db.models import Article, Banner
from util import upload_s3, generate_banner

import requests


async def get_article(article_id: int) -> Article:
    try:
        res = await repo.get_article(article_id)
    except NoResultFound:
        raise HTTPException(status_code=400, detail="Article Not Found.")
    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23503:
            raise HTTPException(status_code=400, detail="Article ID Not Found.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e
    return res


async def get_articles_by_category(category: str) -> list[Article]:
    try:
        res = await repo.get_articles_by_category(category)
        if res is None:
            return []
    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23503:
            raise HTTPException(status_code=400, detail="Category Not Found.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e
    return res


async def get_articles_all() -> list[Article]:
    try:
        res = await repo.get_articles_all()
        if res is None:
            return []
    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23503:
            raise HTTPException(status_code=400, detail="Category Not Found.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e
    return res


async def create_article(article_req: dict) -> Article:
    try:
        # TODO: 광고 이미지 생성 로직 추가
        # banner = await generate_banner(article_req["title"])

        cpg_id = generate_banner.match_with_campaign(article_req["content"])
        campaign_desc = generate_banner.campaigns[cpg_id - 1].get("description")
        res = generate_banner.create_copy(article_req["content"], campaign_desc)
        res = res.split("#######")

        image_url = generate_banner.create_banner("Generate Image of NIKE Snickers with this background: " + res[-1])
        slogan = res[-2]
        desc = res[-3]

        res: Article = await repo.create_article(dict(**article_req, banner_link=image_url, banner_slogan=slogan, banner_desc=desc))

    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23503:
            raise HTTPException(status_code=400, detail="Category Not Found.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e
    return res


async def update_article(article_id: int, article: dict, user_id: int) -> None:
    article = await repo.get_article(article_id)
    if not article.creator_id == user_id:
        raise HTTPException(status_code=403, detail="Not Authorized.")
    try:
        await repo.update_article(article_id, article)
    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23503:
            raise HTTPException(status_code=400, detail="Category Not Found.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e


async def delete_article(article_id: int, user_id: int) -> None:
    try:
        article = await repo.get_article(article_id)
    except NoResultFound:
        raise HTTPException(status_code=400, detail="Article Not Found.")

    if not article.creator_id == user_id:
        raise HTTPException(status_code=403, detail="Not Authorized.")
    try:
        await repo.delete_article(article_id)
    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23503:
            raise HTTPException(status_code=400, detail="Article Not Found.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e

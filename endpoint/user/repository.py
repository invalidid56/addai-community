"""
유저와 관련하여 데이터베이스와 실질적으로 상호작용하는 모듈입니다.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from data.db.database import Transactional
from data.db.models import User


@Transactional()
async def get_user(username: str, session: AsyncSession = None) -> User:
    """
    """
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalars().first()


@Transactional()
async def create_user(user_req: dict, session: AsyncSession = None) -> None:
    """
    """
    _user = User(**user_req)

    session.add(_user)

    await session.commit()
    await session.refresh(_user)


@Transactional()
async def update_user(
    username: str, user_req: dict, session: AsyncSession = None
) -> None:
    """
    """
    stmt = update(User).where(User.username == username).values(**user_req)
    await session.execute(stmt)


@Transactional()
async def delete_user(username: str, session: AsyncSession = None) -> None:
    """
    """
    stmt = delete(User).where(User.username == username)
    await session.execute(stmt)

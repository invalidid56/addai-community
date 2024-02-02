from functools import wraps
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from config import DB_CONFIG, SITE_ENV


SQLALCHEMY_DATABASE_URL = f"{DB_CONFIG['rdb']}://{DB_CONFIG['db_user']}:{DB_CONFIG['db_password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['db']}"


metadata = MetaData()
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Transactional:
    def __call__(self, func):
        @wraps(func)
        async def _transactional(*args, **kwargs):
            async with async_session() as session:
                if kwargs.get("session"):
                    result = await func(*args, **kwargs)
                    await session.commit()
                    return result
                try:
                    kwargs["session"] = session
                    result = await func(*args, **kwargs)
                    await session.commit()
                except Exception as e:
                    # logger.exception(f"{type(e).__name__} : {str(e)}")
                    await session.rollback()
                    raise e
                return result

        return _transactional

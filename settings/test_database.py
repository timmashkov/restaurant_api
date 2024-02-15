from settings.config import test_db_url
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class TestDatabase:
    def __init__(self, url: str, echo: bool) -> None:
        self.test_engine = create_async_engine(url=url, poolclass=NullPool, echo=echo)
        self.test_session_maker = async_sessionmaker(
            bind=self.test_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )


test_database = TestDatabase(test_db_url, echo=True)

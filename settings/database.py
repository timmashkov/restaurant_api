from settings.config import db_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class DataBase:
    def __init__(self, url: str) -> None:
        self._engine = create_async_engine(url=url, echo=False)
        self._session_fabric = async_sessionmaker(
            bind=self._engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def scoped_session(self) -> AsyncSession:
        async with self._session_fabric() as session:
            yield session
            await session.close()


vortex = DataBase(db_url)

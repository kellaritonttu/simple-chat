from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator, Annotated
from fastapi import Depends

from core.config import settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo   = True,
    pool_pre_ping = True,
)


AsyncSessionLocal = async_sessionmaker(
    bind   = async_engine,
    expire_on_commit=False,
    class_ = AsyncSession,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
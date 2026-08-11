import pytest

from httpx import AsyncClient, ASGITransport
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from main import app
from core.config import settings
from database import get_async_session, Base
from schemas.message import MessageCreate
from repository.message import create_message


# ── Database ──────────────────────────────────────────────────────────────────

@pytest.fixture
async def engine():
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(engine):
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
        await session.rollback()


# ── App client ────────────────────────────────────────────────────────────────

@pytest.fixture
async def client(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# ── Message fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
async def saved_message(db_session):
    return await create_message(db_session, MessageCreate(text="Hello world"))
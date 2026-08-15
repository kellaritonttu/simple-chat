import pytest
from unittest.mock import patch, AsyncMock

from httpx import AsyncClient, ASGITransport
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from main import app
from core.config import settings
from database import get_async_session, Base
from schemas.message import MessageCreate
from repository.message import create_message

from repository.user import create_user
from schemas.user import UserCreate

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


# ── Firebase mocking ──────────────────────────────────────────────────────────

@pytest.fixture
def mock_firebase():
    with patch("core.firebase.auth.verify_id_token") as mock:
        mock.return_value = {
            "uid": "test-uid-123",
            "email": "test@example.com"
        }
        yield mock


@pytest.fixture
def mock_firebase_other():
    with patch("core.firebase.auth.verify_id_token") as mock:
        mock.return_value = {
            "uid": "other-uid-456",
            "email": "other@example.com"
        }
        yield mock


# ── User fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture
async def saved_user(db_session):
    """Fixture to create and return a test user."""
    user_data = UserCreate(
        id="test-uid-123",
        google_display_name="Test User",
        app_display_name="Test User"
    )
    user = await create_user(db_session, user_data)
    return user


# ── Message fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
async def saved_message(db_session, saved_user):
    return await create_message(
        db_session,
        MessageCreate(text="Hello world"),
        user_id=saved_user.id
    )


@pytest.fixture(autouse=True)
def mock_broadcast():
    with patch('core.broadcast.message_broadcaster.publish', new_callable=AsyncMock) as mock:
        yield mock
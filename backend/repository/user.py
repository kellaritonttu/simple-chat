from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate


async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    app_display_name = data.app_display_name or data.google_display_name

    user = User(
        id=data.id,
        google_display_name=data.google_display_name,
        app_display_name=app_display_name
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_display_name(db: AsyncSession, user: User, app_display_name: str) -> User:
    user.app_display_name = app_display_name
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()
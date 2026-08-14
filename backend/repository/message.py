from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from models.message import Message
from schemas.message import MessageCreate


async def get_all_messages(db: AsyncSession) -> list[Message]:
    result = await db.execute(
        select(Message)
        .options(selectinload(Message.user))
        .order_by(Message.created_at)
    )
    return result.scalars().all()


async def get_message_by_id(db: AsyncSession, message_id: int) -> Message | None:
    result = await db.execute(
        select(Message)
        .options(selectinload(Message.user))
        .where(Message.id == message_id)
    )
    return result.scalar_one_or_none()


async def create_message(db: AsyncSession, data: MessageCreate, user_id: str) -> Message:
    message = Message(text=data.text, user_id=user_id)
    db.add(message)
    await db.commit()
    result = await db.execute(
        select(Message)
        .options(selectinload(Message.user))
        .where(Message.id == message.id)
    )
    return result.scalar_one()


async def update_message(db: AsyncSession, message: Message, text: str) -> Message:
    message.text = text
    await db.commit()
    result = await db.execute(
        select(Message)
        .options(selectinload(Message.user))
        .where(Message.id == message.id)
    )
    return result.scalar_one()


async def delete_message(db: AsyncSession, message: Message) -> None:
    await db.delete(message)
    await db.commit()
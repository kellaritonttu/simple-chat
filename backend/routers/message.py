from fastapi import APIRouter, HTTPException
from database import AsyncSessionDep
from schemas.message import *
from repository.message import (
    get_all_messages,
    get_message_by_id,
    create_message,
    update_message,
    delete_message,
)

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/", response_model=list[MessageRead])
async def list_messages(db: AsyncSessionDep):
    return await get_all_messages(db)


@router.get("/{message_id}", response_model=MessageRead)
async def get_message(message_id: int, db: AsyncSessionDep):
    message = await get_message_by_id(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@router.post("/", response_model=MessageRead, status_code=201)
async def send_message(data: MessageCreate, db: AsyncSessionDep):
    return await create_message(db, data)


@router.patch("/{message_id}", response_model=MessageRead)
async def edit_message(message_id: int, update: MessageUpdate, db: AsyncSessionDep):
    message = await get_message_by_id(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return await update_message(db, message, update.text)


@router.delete("/{message_id}", status_code=204)
async def remove_message(message_id: int, db: AsyncSessionDep):
    message = await get_message_by_id(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    await delete_message(db, message)
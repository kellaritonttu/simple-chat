import asyncio

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from database import AsyncSessionDep
from schemas.message import *
from repository.message import *
from firebase_admin import auth


from core.firebase import get_current_user
from core.broadcaster import message_broadcaster
from schemas.message import MessageCreate, MessageUpdate, MessageRead


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
async def send_message(
    data: MessageCreate,
    db: AsyncSessionDep,
    current_user: dict = Depends(get_current_user),
):
    message =  await create_message(db, data, user_id=current_user["uid"])

    msg_read = MessageRead.model_validate(message)
    await message_broadcaster.publish("new", msg_read.model_dump(mode="json"))
    return message


@router.patch("/{message_id}", response_model=MessageRead)
async def edit_message(
    message_id: int,
    data: MessageUpdate,
    db: AsyncSessionDep,
    current_user: dict = Depends(get_current_user),
):

    message = await get_message_by_id(db, message_id)

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.user_id != current_user["uid"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    updated = await update_message(db, message, data.text)
    msg_read = MessageRead.model_validate(updated)
    await message_broadcaster.publish("update", msg_read.model_dump(mode="json"))
    return updated


@router.delete("/{message_id}", status_code=204)
async def remove_message(
    message_id: int,
    db: AsyncSessionDep,
    current_user: dict = Depends(get_current_user),
):
    message = await get_message_by_id(db, message_id)

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.user_id != current_user["uid"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    await delete_message(db, message)
    await message_broadcaster.publish("delete", {"id": message_id})


@router.get("/stream")
async def stream_messages(token: str):
    try:
        decoded = auth.verify_id_token(token)
        uid = decoded["uid"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    queue = message_broadcaster.subscribe()

    async def event_generator():
        try:
            yield ":connected\n\n"
            while True:
                msg = await queue.get()
                yield msg
        except asyncio.CancelledError:
            raise
        finally:
            message_broadcaster.unsubscribe(queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
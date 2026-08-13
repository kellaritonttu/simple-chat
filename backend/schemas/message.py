from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    text: str


class MessageUpdate(BaseModel):
    text: str


class MessageRead(BaseModel):
    id:           int
    text:         str
    user_id:      str
    display_name: str | None = None  # joined from users table
    created_at:   datetime
    edited_at:    Optional[datetime] = None

    model_config = {"from_attributes": True}
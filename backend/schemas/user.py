from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    id: str  # Firebase UID
    google_display_name: str
    app_display_name:    str


class UserRead(BaseModel):
    id: str
    google_display_name: str
    app_display_name:    str
    created_at:          datetime
    edited_at:           datetime | None = None

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    app_display_name: str
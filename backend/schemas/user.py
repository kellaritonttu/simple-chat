from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    id:           str  # Firebase UID
    display_name: str


class UserRead(BaseModel):
    id:           str
    display_name: str
    created_at:   datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    display_name: str
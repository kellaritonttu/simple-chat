from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id:                  Mapped[str]      = mapped_column(primary_key=True)  # Firebase UID

    google_display_name: Mapped[str]
    app_display_name:    Mapped[str]

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    edited_at:  Mapped[Optional[datetime]] = mapped_column(
        default  = None,
        onupdate = func.now()
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        cascade="all, delete-orphan",
        back_populates="user"
    )
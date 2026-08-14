from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func
from datetime import datetime
from database import Base

from models.user import User

class Message(Base):
    __tablename__ = "messages"

    id:         Mapped[int] = mapped_column(primary_key=True)
    text:       Mapped[str]
    user_id:    Mapped[str] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    edited_at:  Mapped[Optional[datetime]] = mapped_column(
        default=None,
        onupdate=func.now()
    )

    user: Mapped[User] = relationship("User", back_populates="messages")

    @property
    def display_name(self) -> str | None:
        return self.user.app_display_name if self.user else None
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id:           Mapped[str]      = mapped_column(primary_key=True)  # Firebase UID
    display_name: Mapped[str]
    created_at:   Mapped[datetime] = mapped_column(server_default=func.now())
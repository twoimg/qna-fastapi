from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from app.core.database.base import Base

from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.question import Question
    from app.models.answer import Answer
    
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String())
    
    bio: Mapped[str] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    questions: Mapped[list["Question"]] = relationship(back_populates="user")
    answers: Mapped[list["Answer"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"

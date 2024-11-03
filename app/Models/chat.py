from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app import db

class Chat(db.Model):
    __tablename__ = 'chat'

    chatID: Mapped[int] = mapped_column(primary_key=True)
    user1: Mapped[str] = mapped_column(String(255), unique=True)
    user2: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column()


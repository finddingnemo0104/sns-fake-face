from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db
from app.Models.message import Message


class Chat(db.Model):
    __tablename__ = 'chat'

    chatID: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column()

    messages: Mapped[List["Message"]] = relationship(back_populates="chat", lazy=True)
    chat_users: Mapped[List["ChatUser"]] = relationship(back_populates="chat", lazy=True)

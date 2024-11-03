from datetime import datetime

from sqlalchemy import String, TEXT
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class Message(db.Model):
    __tablename__ = 'messsage'

    messageID: Mapped[int] = mapped_column(primary_key=True)
    chatID: Mapped[str] = mapped_column(String(255), unique=True)
    senderID: Mapped[str] = mapped_column(String(255), unique=True)
    context: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column()


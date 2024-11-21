from datetime import datetime

from sqlalchemy import String, TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class Message(db.Model):
    __tablename__ = 'messsage'

    messageID: Mapped[int] = mapped_column(primary_key=True)
    chatID: Mapped[str] = mapped_column(ForeignKey('chat.chatID'), nullable=False)
    senderID: Mapped[str] = mapped_column(ForeignKey('user.id'), nullable=False)
    content: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column()

    chat: Mapped["Chat"] = relationship(back_populates="messages")
    sender: Mapped["User"] = relationship(back_populates="messages")

    def save(self):
        db.session.add(self)
        db.session.commit()

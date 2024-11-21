from sqlalchemy import String, TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db
from app.Models.chat import Chat
from app.Models.message import Message

class ChatUser(db.Model):
    __tablename__ = 'chat_user'

    chatUserID: Mapped[int] = mapped_column(primary_key=True)
    chatID: Mapped[str] = mapped_column(ForeignKey('chat.chatID'), nullable=False)
    userID: Mapped[str] = mapped_column(ForeignKey('user.id'), nullable=False)

    chat: Mapped["Chat"] = relationship("Chat", back_populates="chat_users")
    user: Mapped["User"] = relationship("User", back_populates="chat_users")

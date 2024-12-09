from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, DateTime

from app import db


class Commemt(db.Model):
    __tablename__ = 'comment'
    commentID: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    userID: Mapped[int] = mapped_column()
    postID: Mapped[int] = mapped_column()
    create_at: Mapped[DateTime] = mapped_column()
    update_at: Mapped[DateTime] = mapped_column()
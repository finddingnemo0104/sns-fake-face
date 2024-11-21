from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db
from app.Models.user import User


class Post(db.Model):
    __tablename__ = 'post'
    postID: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(255))
    image: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column()

    userID: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    User: Mapped["User"] = relationship("User", back_populates="posts")

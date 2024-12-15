from datetime import datetime

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db
from app.Models.user import User


class Post(db.Model):
    __tablename__ = 'post'
    postID: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    image: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column(nullable = True)
    totalLikes: Mapped[int] = mapped_column(default=0)
    totalComments: Mapped[int] = mapped_column(default=0)

    userID: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    User: Mapped["User"] = relationship("User", back_populates="posts")

    comments = relationship("Comment", back_populates="post", lazy=True, cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", lazy=True, cascade="all, delete-orphan")


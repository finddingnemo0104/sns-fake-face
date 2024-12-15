from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey
from datetime import datetime

from app import db
from app.Models.user import User
from app.Models.post import Post


class Comment(db.Model):
    __tablename__ = 'comment'
    commentID: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    create_at: Mapped[datetime] = mapped_column()
    update_at: Mapped[datetime] = mapped_column()

    userID: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="comments")

    postID: Mapped[int] = mapped_column(ForeignKey('post.postID'), nullable=False)
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

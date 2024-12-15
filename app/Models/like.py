from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from app import db
from app.Models.user import User
from app.Models.post import Post


class Like(db.Model):
    __tablename__ = 'like'

    likeID: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Mối quan hệ với User
    userID: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="likes")

    # Mối quan hệ với Post
    postID: Mapped[int] = mapped_column(ForeignKey('post.postID'), nullable=False)
    post: Mapped["Post"] = relationship("Post", back_populates="likes")

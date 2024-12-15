from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db
from app.Models.user import User


class Friendship(db.Model):
    __tablename__ = 'friendship'

    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    friendId: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    status: Mapped[str] = mapped_column(String(255), default="pending")  # pending, accepted, blocked

    user: Mapped["User"] = relationship("User", foreign_keys=[userId])
    friend: Mapped["User"] = relationship("User", foreign_keys=[friendId])
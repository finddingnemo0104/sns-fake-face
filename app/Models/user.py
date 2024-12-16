from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import String, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    gender: Mapped[str] = mapped_column(String(255))
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    dob: Mapped[datetime] = mapped_column()
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()

    messages = relationship("Message", back_populates="sender", lazy=True, cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", lazy=True, cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", lazy=True, cascade="all, delete-orphan")
    chat_users = relationship("ChatUser", back_populates="user", lazy=True, cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="User", lazy=True, cascade="all, delete-orphan")
    friendships_as_user = relationship(
        "Friendship", foreign_keys="[Friendship.userId]", back_populates="user", lazy=True, cascade="all, delete-orphan"
    )
    friendships_as_friend = relationship(
        "Friendship", foreign_keys="[Friendship.friendId]", back_populates="friend", lazy=True, cascade="all, delete-orphan"
    )

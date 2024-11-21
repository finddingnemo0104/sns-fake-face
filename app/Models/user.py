from datetime import datetime
from typing import List

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
    cover: Mapped[str] = mapped_column(String(255), nullable=True)
    dob: Mapped[datetime] = mapped_column()
    biography: Mapped[str] = mapped_column(TEXT, nullable=True)
    phone: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()

    messages = relationship("Message", back_populates="sender", lazy=True)
    chat_users = relationship("ChatUser", back_populates="user", lazy=True)
    posts = relationship("Post", back_populates="User", lazy=True)

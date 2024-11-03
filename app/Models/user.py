from datetime import datetime

from sqlalchemy import String, TEXT
from sqlalchemy.orm import Mapped, mapped_column
from app import db


class User(db.Model):
    __tablename__ = 'user'

    userID: Mapped[int] = mapped_column(primary_key=True)
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


def create_user():
    user = User(
        userID=1,
        username="thuytrang",
        password="123456",
        name="Thuy Trang",
        gender="Female",
        avatar="",
        cover="",
        dob=datetime.now(),
        biography="",
        phone="0123456789",
        email="thuytrang@gmail.com",
        created_at=datetime.now(),
        updated_at=datetime.now(),)

    db.session.add(user)
    db.session.commit()


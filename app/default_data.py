from datetime import datetime, timedelta

from app import db
from app.Models.chat import Chat
from app.Models.chat_user import ChatUser
from app.Models.message import Message
from app.Models.post import Post
from app.Models.user import User
import random


def add_default_data():
    if not db.session.execute(db.select(User)).scalar():
        user_1 = User(username="thuyTrang", password="123456", name="Thuy Trang", gender="Female", avatar="/static/image/no-avatar.jpg", dob=datetime(1990, 1, 1), email="user1@example.com", created_at=datetime.now(), updated_at=datetime.now())
        user_2 = User(username="nguyenHa", password="123456", name="Nguyễn Hà", gender="Female", avatar="/static/image/no-avatar.jpg", dob=datetime(1990, 1, 1), email="user2@example.com", created_at=datetime.now(), updated_at=datetime.now())
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()

        users = [
            User(
                username="phuongThao",
                password="password1",
                name="Phương Thảo",
                gender="Female",
                avatar="/static/image/no-avatar.jpg",
                dob=datetime(1995, 5, 10),
                email="phuongthao@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            User(
                username="minhAnh",
                password="password2",
                name="Minh Anh",
                gender="Male",
                avatar="/static/image/no-avatar.jpg",
                dob=datetime(1992, 3, 15),
                email="minhanh@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            User(
                username="quocBao",
                password="password3",
                name="Quốc Bảo",
                gender="Male",
                avatar="/static/image/no-avatar.jpg",
                dob=datetime(1990, 12, 25),
                email="quocbao@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            User(
                username="baoNgoc",
                password="password4",
                name="Bảo Ngọc",
                gender="Female",
                avatar="/static/image/no-avatar.jpg",
                dob=datetime(1998, 7, 19),
                email="baongoc@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            User(
                username="tuanKiet",
                password="password5",
                name="Tuấn Kiệt",
                gender="Male",
                avatar="/static/image/no-avatar.jpg",
                dob=datetime(1988, 11, 2),
                email="tuankiet@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            User(
                username="hoangLong",
                password="password6",
                name="Hoàng Long",
                gender="Male",
                avatar="/static/image/no-avatar.jpg",
                dob=datetime(1996, 4, 18),
                email="hoanglong@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            User(
                username="baoTram",
                password="password7",
                name="Bảo Trâm",
                gender="Female",
                avatar="/static/image/no-avatar.jpg",
                dob=datetime(1997, 6, 9),
                email="baotram@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            User(
                username="kimDung",
                password="password8",
                name="Kim Dung",
                gender="Female",
                avatar="/static/image/no-avatar.jpg",
                dob=datetime(1993, 8, 20),
                email="kimdung@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            User(
                username="haiNam",
                password="password9",
                name="Hải Nam",
                gender="Male",
                avatar="/static/image/no-avatar.jpg",
                dob=datetime(1991, 10, 5),
                email="hainam@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            User(
                username="thanhVan",
                password="password10",
                name="Thanh Vân",
                gender="Female",
                avatar="/static/image/no-avatar.jpg",
                dob=datetime(1994, 2, 28),
                email="thanhvan@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            User(
                username="ngocAnh",
                password="password11",
                name="Ngọc Anh",
                gender="Female",
                avatar="/static/image/no-avatar.jpg",
                dob=datetime(1995, 9, 12),
                email="ngocanh@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            User(
                username="duongLam",
                password="password12",
                name="Dương Lâm",
                gender="Male",
                avatar="/static/image/no-avatar.jpg",
                dob=datetime(1990, 1, 30),
                email="duonglam@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        ]

        # Add users to the session
        for user in users:
            db.session.add(user)

        # Commit to the database
        db.session.commit()


        chat = Chat(created_at=datetime.now())
        db.session.add(chat)
        db.session.commit()

        chat_user_1 = ChatUser(chatID=chat.chatID, userID=1)
        chat_user_2 = ChatUser(chatID=chat.chatID, userID=2)
        db.session.add(chat_user_1)
        db.session.add(chat_user_2)
        db.session.commit()

        message = Message(chatID=chat.chatID, senderID=1, content="Hello", created_at=datetime.now())
        db.session.add(message)
        db.session.commit()

        # Danh sách nội dung và URL ảnh
        posts = [
            {"content": "Bài đăng đầu tiên yeah~",
             "image": "https://images.pexels.com/photos/1391501/pexels-photo-1391501.jpeg"},
            {"content": "Những khoảnh khắc đáng nhớ luôn đến từ những điều giản dị.",
             "image": "https://images.unsplash.com/photo-1732740676396-ece9a9148342?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
            {"content": "Tình yêu là ánh sáng dẫn lối qua những ngày u tối.",
             "image": "https://images.unsplash.com/photo-1732762990635-a713a09e9025?q=80&w=1936&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
            {"content": "Hạnh phúc đến từ việc chia sẻ những điều nhỏ bé.",
             "image": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d"},
            {"content": "Mỗi ngày đều là một cơ hội để bắt đầu lại từ đầu.",
             "image": "https://images.unsplash.com/photo-1732763200110-7d7581f3bea4?q=80&w=1936&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
            {"content": "Cây cối cũng như con người, cần thời gian để lớn mạnh.",
             "image": "https://images.pexels.com/photos/1237119/pexels-photo-1237119.jpeg"},
            {"content": "Ngọn núi cao luôn là đích đến của những người dũng cảm.",
             "image": "https://plus.unsplash.com/premium_photo-1682949695409-5e5a5a7f6b72?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
            {"content": "Tình bạn là ánh sáng xuyên qua bóng tối của cuộc đời.",
             "image": "https://images.unsplash.com/photo-1472491235688-bdc81a63246e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
            {"content": "Hành trình xa nhất bắt đầu từ bước đi đầu tiên.",
             "image": "https://images.unsplash.com/photo-1500259571355-332da5cb07aa?q=80&w=1888&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
            {"content": "Tâm hồn cần những khoảnh khắc yên bình để được chữa lành.",
             "image": "https://images.pexels.com/photos/1714208/pexels-photo-1714208.jpeg"},
         ]

        base_date = datetime.now() - timedelta(days=10)  # Ngày bắt đầu (10 ngày trước)
        for i, post in enumerate(posts, start=1):
            created_at = base_date + timedelta(days=i, seconds=random.randint(0, 86400))

            new_post = Post(
                postID=i,
                content=post["content"],
                image=post["image"],
                created_at=created_at,
                updated_at=None,
                userID=random.randint(1, 12)
            )
            db.session.add(new_post)
        db.session.commit()




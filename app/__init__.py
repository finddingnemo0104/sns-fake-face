from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()


def create_app():
    from app.routes.socketio import socketio_events
    from werkzeug.utils import secure_filename

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:khongrotmon@localhost:3306/sns_fake_face"
    app.config["SECRET_KEY"] = "mysecret"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    socketio_events(socketio)

    from app.Models.user import User
    from app.Models.message import Message
    from app.Models.chat_user import ChatUser
    from app.Models.chat import Chat
    from app.Models.post import Post

    with app.app_context():
        db.create_all()

        # if chat is empty, create a new chat
        if not db.session.execute(db.select(User)).scalar():
            user_1 = User(username="thuyTrang", password="123456", name="Thuy Trang", gender="Female", avatar=None, cover=None, dob=datetime(1990, 1, 1), biography=None, phone="1234567890", email="user1@example.com", created_at=datetime.now(), updated_at=datetime.now())
            user_2 = User(username="trangThuy", password="123456", name="Trang Thuy", gender="Female", avatar=None, cover=None, dob=datetime(1990, 1, 1), biography=None, phone="1234567890", email="user1@example.com", created_at=datetime.now(), updated_at=datetime.now())
            db.session.add(user_1)
            db.session.add(user_2)
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

    from app.routes.main import main_bp
    from app.routes.auth import authentication_bp
    from app.routes.post import post_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(authentication_bp)
    app.register_blueprint(post_bp)
    return app

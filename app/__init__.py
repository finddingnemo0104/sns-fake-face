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
    from app.Models.friendship import Friendship
    from app.Models.comment import Comment
    from app.Models.like import Like

    with app.app_context():
        db.create_all()

        # if chat is empty, create a new chat
        from app.default_data import add_default_data
        add_default_data()


    from app.routes.main import main_bp
    from app.routes.auth import authentication_bp
    from app.routes.post import post_bp
    from app.routes.user import user_bp
    from app.routes.comment import comment_bp
    from app.routes.chats import chats_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(authentication_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(chats_bp)
    return app

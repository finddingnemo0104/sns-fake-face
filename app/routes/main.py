from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, current_app
from flask_login import  login_required

from app import db, login_manager
from app.Models.chat import Chat
from app.Models.chat_user import ChatUser
from app.Models.user import User
from flask_login import current_user

main_bp = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main_bp.route('/')
def home():  # put application's code here
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))

    return redirect(url_for('authentication.login_page'))


@main_bp.route('/chats')
def message_page():
    if not current_user.is_authenticated:
        return render_template('login.html')

    chatID = request.args.get('chatID')
    chats = Chat.query.all()
    # query the chat that the user is in
    if chatID is not None:
        current_chat = Chat.query.get(chatID)
        # get the other user in the chat
        chat_user = ChatUser.query.filter_by(chatID=chatID).filter(ChatUser.userID != current_user.id).scalar()
        chat_partner = chat_user.user
        # get the messages in the chat
        messages = current_chat.messages
        return render_template('message.html', chats=chats, current_chat=current_chat, chat_partner=chat_partner,
                               messages=messages)

    return render_template('message.html', chats=chats)


@main_bp.route('/home')
def home_page():
    print(current_user)
    return render_template('home.html')


@main_bp.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)

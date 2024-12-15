from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, current_app, jsonify
from flask_login import  login_required

from app import db, login_manager
from app.Models.chat import Chat
from app.Models.chat_user import ChatUser
from app.Models.friendship import Friendship
from app.Models.user import User
from flask_login import current_user

from app.routes.user import get_friendship_json

main_bp = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main_bp.route('/')
@login_required
def home():
    friend_requests = Friendship.query.filter(
        ((Friendship.friendId == current_user.id) & (Friendship.status == "pending")) |
        ((Friendship.userId == current_user.id) & (Friendship.status == "pending"))
    ).all()
    return render_template('home.html', friend_requests=friend_requests)





@main_bp.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)

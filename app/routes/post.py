import os
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, json, jsonify, current_app, \
    send_from_directory
from flask_login import  login_required
from werkzeug.utils import secure_filename

from app import db, login_manager, ALLOWED_EXTENSIONS
from app.Models.post import Post
from app.Models.chat import Chat
from app.Models.chat_user import ChatUser
from app.Models.user import User
from flask_login import current_user

post_bp = Blueprint('post', __name__)


@post_bp.route('/posts')
@login_required
def post_page():
    posts = Post.query.order_by(Post.created_at.desc()).all()

    posts_json = [
        {
            "postID": post.postID,
            "content": post.content,
            "image": post.image,
            "created_at": post.created_at,
            "user": {
                "id": post.User.id,
                "name": post.User.name
            }
        } for post in posts
    ]

    return jsonify(posts_json)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@post_bp.route('/posts/create', methods=['POST'])
@login_required
def create_post():
    content = request.form['content']
    fileImage = request.files.get('image')
    image = ''

    if fileImage and allowed_file(fileImage.filename):
        filename = secure_filename(fileImage.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)  # Đường dẫn đầy đủ của file
        fileImage.save(filepath)
        image = "/static/uploads/" + filename

    post = Post(content=content, image=image, userID=current_user.id, created_at=datetime.now())
    db.session.add(post)
    db.session.commit()

    post_json = {
        "postID": post.postID,
        "content": post.content,
        "image": post.image,
        "created_at": post.created_at,
        "user": {
            "id": post.User.id,
            "name": post.User.name
        }
    }

    return jsonify(post_json)



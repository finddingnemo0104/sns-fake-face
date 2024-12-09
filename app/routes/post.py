import os
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from app import db, ALLOWED_EXTENSIONS
from app.Models.post import Post
from flask_login import current_user

post_bp = Blueprint('post', __name__)


@post_bp.route('/posts')
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


@post_bp.route('/posts/delete/<id>', methods=['DELETE'])
def delete_post(id):
    db.session.query(Post).filter_by(postID=id).delete()
    db.session.commit()
    return jsonify({'message': 'success'})


@post_bp.route('/post/<id>', methods=['GET'])
def get_post(id):
    post = db.session.query(Post).filter_by(postID=id).first()
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


@post_bp.route('/post/update/<id>', methods=['PATCH'])
def update_post(id):
    content = request.form['content']
    previewImage = request.form['previewImage']
    fileImage = request.files.get('image')
    image = ''

    if fileImage and allowed_file(fileImage.filename):
        filename = secure_filename(fileImage.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)  # Đường dẫn đầy đủ của file
        fileImage.save(filepath)
        image = "/static/uploads/" + filename

    post = db.session.query(Post).filter_by(postID=id).first()
    post.content = content
    # Upload new image
    if image != '':
        post.image = image
    else:
        # Remove image
        if previewImage == '':
            post.image = ''

    post.updated_at = datetime.now()
    db.session.commit()
    post_json = {
        "postID": post.postID,
        "content": post.content,
        "image": post.image,
        "created_at": post.created_at,
        "upated_at":  post.updated_at,
        "user": {
            "id": post.User.id,
            "name": post.User.name
        }
    }
    return jsonify(post_json)

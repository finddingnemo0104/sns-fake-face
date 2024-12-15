import os
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app, render_template
from werkzeug.utils import secure_filename

from app import db, ALLOWED_EXTENSIONS
from app.Models.like import Like
from app.Models.post import Post
from flask_login import current_user, login_required
from sqlalchemy import desc, asc

post_bp = Blueprint('post', __name__)

def get_post_json(post):
    post_json = {
        "postID": post.postID,
        "content": post.content,
        "image": post.image,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "user": {
            "id": post.User.id,
            "name": post.User.name,
            "avatar": post.User.avatar,
        },
        'comments': [
            {
                "commentID": comment.commentID,
                "content": comment.content,
                "postID": comment.postID,
                "create_at": comment.create_at,
                "update_at": comment.update_at,
                "user": {
                    "id": comment.user.id,
                    "name": comment.user.name,
                    "avatar": comment.user.avatar,
                },
                'isOwner': comment.user.id == current_user.id,
            } for comment in post.comments
        ],
        'totalLikes': post.totalLikes,
        'totalComments': post.totalComments
    }
    return post_json


@post_bp.route('/posts')
@login_required
def get_posts():
    # get query parameter of page and limit
    # default page = 1, limit = 5
    # page means the current page
    page = request.args.get('page', 1, type=int)
    # limit means the number of posts per page
    limit = request.args.get('limit', 5, type=int)
    profileId = request.args.get('profileId', type=int)
    if profileId is None:
        # query all posts and order by created_at desc and paginate by page and limit
        posts_query = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=limit)
    else:
        posts_query = Post.query.filter_by(userID=profileId).order_by(Post.created_at.desc()).paginate(page=page, per_page=limit)


    total_of_post = posts_query.total
    posts = posts_query.items

    posts_json = {
        "total": total_of_post,
        "posts": []
    }

    for post in posts:
        # Check if current_user has liked this post
        liked = db.session.query(Like).filter_by(userID=current_user.id, postID=post.postID).first() is not None

        # Add the liked attribute to each post's JSON representation
        post_json = get_post_json(post)
        post_json['liked'] = liked

        if post.userID == current_user.id:
            post_json['isOwner'] = True
        else:
            post_json['isOwner'] = False

        posts_json["posts"].append(post_json)

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

    return jsonify(get_post_json(post))


@post_bp.route('/posts/detail/<int:postID>', methods=['GET'])
@login_required
def detail_post_page(postID):
    post = db.session.query(Post).filter_by(postID=postID).first()
    return render_template("detail-post.html", post=post)


@post_bp.route('/posts/delete/<id>', methods=['DELETE'])
@login_required
def delete_post(id):
    db.session.query(Post).filter_by(postID=id).delete()
    db.session.commit()
    return jsonify({'message': 'success'})


@post_bp.route('/post/<id>', methods=['GET'])
@login_required
def get_post(id):
    post = db.session.query(Post).filter_by(postID=id).first()
    return jsonify(get_post_json(post))


@post_bp.route('/post/update/<id>', methods=['PATCH'])
@login_required
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
    return jsonify(get_post_json(post))


@post_bp.route("/posts/like/<int:postID>", methods=['GET'])
@login_required
def like_post(postID):
    post = db.session.query(Post).filter_by(postID=postID).first()

    # Kiểm tra xem bài viết có tồn tại không
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    # Kiểm tra nếu người dùng đã thích bài viết này chưa
    existing_like = db.session.query(Like).filter_by(userID=current_user.id, postID=postID).first()

    if existing_like:
        # Nếu đã like, thì hủy like
        db.session.delete(existing_like)
        post.totalLikes -= 1
    else:
        # Nếu chưa like, thêm like mới
        like = Like(userID=current_user.id, postID=postID)
        db.session.add(like)
        post.totalLikes += 1

    # Commit thay đổi và trả về tổng số lượt like mới
    db.session.commit()

    return jsonify({
        'totalLikes': post.totalLikes,
        'liked': not existing_like  # Trả về true nếu người dùng đã thích, false nếu đã hủy
    })

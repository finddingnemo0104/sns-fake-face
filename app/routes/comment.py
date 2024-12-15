from datetime import datetime

from flask import Blueprint, request, jsonify

from app import db
from app.Models.comment import Comment
from flask_login import current_user, login_required

from app.Models.post import Post

comment_bp = Blueprint('comment', __name__)


def get_comment_json(comment):
    return {
        "commentID": comment.commentID,
        "content": comment.content,
        "postID": comment.postID,
        "create_at": comment.create_at,
        "update_at": comment.update_at,
        "user": {
            "id": comment.user.id,
            "name": comment.user.name,
            "avatar": comment.user.avatar,
        }
    }


@comment_bp.route('/comments', methods=['GET'])
@login_required
def get_comments():
    pass


@comment_bp.route('/comments/create', methods=['POST'])
@login_required
def create_comment():
    content = request.form['content']
    postID = request.form['postID']
    comment = Comment(content=content, create_at=datetime.now(), update_at=datetime.now(), postID=postID,
                      userID=current_user.id)
    db.session.add(comment)
    post = Post.query.filter_by(postID=postID).first()
    post.totalComments += 1
    db.session.commit()
    comments_json = get_comment_json(comment)
    comments_json['totalComments'] = post.totalComments
    return jsonify(comments_json)


@comment_bp.route('/comments/delete/<int:commentID>', methods=['DELETE'])
@login_required
def delete_comment(commentID):
    comment = Comment.query.get(commentID)
    post = Post.query.filter_by(postID=comment.postID).first()
    post.totalComments -= 1
    db.session.delete(comment)
    db.session.commit()
    return jsonify({
        'commentID': commentID,
        'success': True,
        'totalComments': post.totalComments
    })
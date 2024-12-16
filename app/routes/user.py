import os
from datetime import datetime

from flask import Blueprint, url_for, redirect, request, render_template, jsonify, current_app
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy.exc import NoResultFound
from werkzeug.utils import secure_filename

from app import db, login_manager
from app.Models.friendship import Friendship
from app.Models.user import User
from app.routes.post import allowed_file

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile/<int:userID>')
@login_required
def profile_page(userID):
    if userID is None:
        return redirect(url_for('main.home'))

    # Fetch the user whose profile is being visited
    user = User.query.get(userID)
    if not user:
        return "User not found", 404

    # Check the friendship status
    friendship = Friendship.query.filter(
        ((Friendship.userId == current_user.id) & (Friendship.friendId == userID)) |
        ((Friendship.userId == userID) & (Friendship.friendId == current_user.id))
    ).first()

    if not friendship:
        friendshipButtonText = "Kết bạn"  # No friendship exists
    elif friendship.userId == userID and friendship.status == "pending":
        friendshipButtonText = "Chấp nhận"  # Other user has sent a friend request
    elif friendship.friendId == userID and friendship.status == "pending":
        friendshipButtonText = "Hủy lời mời"  # Other user has sent a friend request
    elif friendship.status == "accepted":
        friendshipButtonText = "Bạn bè"  # Already friends
    else:
        friendshipButtonText = "Kết bạn"  # Default case (e.g., blocked or unexpected states)

    # Get friends of profile
    profileFriendship = Friendship.query.filter(
        ((Friendship.friendId == userID) & (Friendship.status == "accepted")) |
        ((Friendship.userId == userID) & (Friendship.status == "accepted"))
    ).all()

    # Extract only the friends as User objects, excluding the current_user
    profileFriends = [
        friendship.user if friendship.friendId == userID else friendship.friend
        for friendship in profileFriendship
    ]
    totalFriends = len(profileFriends)

    user.dob = datetime.strftime(user.dob, '%Y-%m-%d')

    return render_template('profile.html', user=user, friendshipButtonText=friendshipButtonText,
                           profileFriends=profileFriends, totalFriends=totalFriends)


@user_bp.route('/friend-request/<friendID>', methods=['GET', 'POST'])
@login_required
def send_friend_request(friendID):
    if friendID is not None:
        # check if already sent request
        friendship = Friendship.query.filter_by(userId=current_user.id, friendId=friendID).scalar()
        if friendship and friendship.status == 'pending':
            db.session.delete(friendship)
            db.session.commit()
            return jsonify({"message": 'Kết bạn'})

        newFriendship = Friendship(userId=current_user.id, friendId=friendID)
        db.session.add(newFriendship)
        db.session.commit()
        return jsonify({"message": 'Đã gửi lời mời kết bạn'})
    return redirect(url_for('main.home'))


@user_bp.route('/friend-request/', methods=['GET'])
@login_required
def get_friend_requests():
    friend_requests = Friendship.query.filter_by(friendId=current_user.id).all()
    friend_requests_json = [
        get_friendship_json(friendship) for friendship in friend_requests
    ]
    return jsonify(friend_requests_json)


@user_bp.route('/friend-request/<int:friendID>/reject', methods=['GET'])
@login_required
def reject_friend_request(friendID):
    if friendID is not None:
        # check if already sent request
        friendship = Friendship.query.filter_by(userId=friendID, friendId=current_user.id).first()
        friendship = Friendship.query.filter(
            ((Friendship.userId == current_user.id) & (Friendship.friendId == friendID)) |
            ((Friendship.userId == friendID) & (Friendship.friendId == current_user.id))
        ).first()
        if friendship:
            db.session.delete(friendship)
            db.session.commit()
            return redirect(url_for('user.profile_page', userID=friendID))

    return redirect(url_for('main.home'))


@user_bp.route('/friend-request/<int:friendID>/accept', methods=['GET'])
@login_required
def accept_friend_request(friendID):
    if friendID is not None:
        friendship = Friendship.query.filter_by(userId=friendID, friendId=current_user.id).first()
        if friendship:
            friendship.status = "accepted"
            db.session.commit()
            return redirect(url_for('user.profile_page', userID=friendID))

    return redirect(url_for('main.home'))


@user_bp.route('/profile/<int:userID>/friends', methods=['GET'])
@login_required
def list_friends_page(userID):
    if userID is None:
        return redirect(url_for('main.home'))

    # Fetch the user whose profile is being visited
    user = User.query.get(userID)
    if not user:
        return "User not found", 404

    # Get friends of profile
    profileFriendship = Friendship.query.filter(
        (Friendship.friendId == userID) |
        (Friendship.userId == userID)
    ).all()

    # Extract only the friends as User objects, excluding the current_user
    profileFriends = [
        friendship.user if friendship.friendId == userID else friendship.friend
        for friendship in profileFriendship
    ]
    totalFriends = len(profileFriends)

    return render_template("list_friend.html", profile=user, profileFriends=profileFriends, totalFriends=totalFriends)


@user_bp.route('/users/delete/<int:userID>', methods=['GET'])
@login_required
def delete_user(userID):
    if current_user.id != userID:
        return "You are not authorized to delete this user", 403

    user = User.query.get(userID)
    if not user:
        return "User not found", 404


    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.home'))


@user_bp.route('/users/detail/<int:userID>', methods=['GET'])
@login_required
def get_user_by_id(userID):
    user = User.query.get(userID)
    if not user:
        return "User not found", 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        'dob': user.dob,
        'email': user.email,
        'gender': user.gender,
    })

@user_bp.route('/users/update/<int:userID>', methods=['POST'])
@login_required
def update_user(userID):
    user = User.query.get(userID)
    dob = request.form['dob']
    email = request.form['email']
    gender = request.form['gender']

    dob = datetime.strptime(dob, '%Y-%m-%d')

    user.dob = dob
    user.email = email
    user.gender = gender

    db.session.commit()
    return redirect(url_for('user.profile_page', userID=userID))


@user_bp.route('/users/update-avatar/', methods=['POST'])
@login_required
def update_avatar():
    user = User.query.get(current_user.id)
    fileImage = request.files.get('avatar')
    avatar = ''

    if fileImage and allowed_file(fileImage.filename):
        filename = secure_filename(fileImage.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)  # Đường dẫn đầy đủ của file
        fileImage.save(filepath)
        avatar = "/static/uploads/" + filename

    user.avatar = avatar

    db.session.commit()
    return redirect(url_for('user.profile_page', userID=current_user.id))


def get_friendship_json(friendship):
    friendship_json = {
        'id': friendship.id,
        'userId': friendship.userId,
        'friendId': friendship.friendId,
        'status': friendship.status,
        'user': {
            'id': friendship.user.id,
            'name': friendship.user.name,
            'avatar': friendship.user.avatar,
        },
        'friend': {
            'id': friendship.friend.id,
            'name': friendship.friend.name,
            'avatar': friendship.friend.avatar,
        }
    }
    return friendship_json

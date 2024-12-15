from datetime import datetime

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.Models.chat import Chat
from app.Models.chat_user import ChatUser

chats_bp = Blueprint('chats', __name__)

@chats_bp.route('/chats')
@login_required
def message_page():
    chatID = request.args.get('chatID')

    # Lấy tất cả các đoạn chat của current_user
    user_chats = db.session.query(Chat, ChatUser).join(ChatUser, Chat.chatID == ChatUser.chatID).filter(
        ChatUser.userID == current_user.id
    ).all()

    # Tạo danh sách chat kèm dữ liệu người chung chat
    # Kiểu dữ liệu của chats_with_users
    # {
    #   chat: chat
    #   partner: partner
    # }
    chats_with_users = []
    for chat, chat_user in user_chats:
        # Lấy người chung chat (người không phải current_user)
        other_user = db.session.query(ChatUser).filter(
            ChatUser.chatID == chat.chatID,
            ChatUser.userID != current_user.id
        ).first()

        if other_user:
            chats_with_users.append({
                'chat': chat,
                'partner': other_user.user  # Lấy dữ liệu User của người chung chat
            })

    # Nếu có chatID, lấy chi tiết đoạn chat đó
    if chatID is not None:
        current_chat = Chat.query.get_or_404(chatID)
        chat_user = ChatUser.query.filter_by(chatID=chatID).filter(ChatUser.userID != current_user.id).first()
        chat_partner = chat_user.user if chat_user else None
        messages = current_chat.messages

        return render_template(
            'message.html',
            chats=chats_with_users,
            current_chat=current_chat,
            chat_partner=chat_partner,
            messages=messages
        )

    # Nếu không có chatID, chỉ hiển thị danh sách chat
    return render_template('message.html', chats=chats_with_users)


@chats_bp.route('/chats/create/<int:userID>', methods=['GET'])
@login_required
def create_chat(userID):
    # Kiểm tra nếu hai người dùng đã có chung một chat
    existing_chat = db.session.query(ChatUser.chatID).filter(
        ChatUser.userID == current_user.id  # User hiện tại
    ).filter(
        ChatUser.chatID.in_(  # ChatID mà user kia cũng tham gia
            db.session.query(ChatUser.chatID).filter(ChatUser.userID == userID)
        )
    ).first()

    if existing_chat:
        return redirect(url_for('chats.message_page', chatID=[existing_chat.chatID]))

    chat = Chat(created_at=datetime.now())
    db.session.add(chat)
    db.session.commit()


    chat_user_1 = ChatUser(chatID=chat.chatID, userID=current_user.id)
    chat_user_2 = ChatUser(chatID=chat.chatID, userID=userID)

    db.session.add(chat_user_1)
    db.session.add(chat_user_2)
    db.session.commit()

    return redirect(url_for("chats.message_page", chatID=[chat.chatID]))
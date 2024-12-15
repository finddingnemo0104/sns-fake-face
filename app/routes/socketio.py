from datetime import datetime

from flask_login import current_user
from flask_socketio import join_room, leave_room, send, emit

from app.Models.message import Message


def socketio_events(socketio):
    @socketio.on("connect")
    def handle_connect():
        print(f"Client connected: {current_user.username}")

    @socketio.on("disconnect")
    def handle_disconnect():
        print("Client disconnected")

    @socketio.on('message')
    def handle_message(jsonData):
        if not current_user.is_authenticated:
            return False

        chatID = int(jsonData['chatID'])
        userId = int(jsonData['userID'])
        messageContent = jsonData['message']

        if userId != current_user.id:
            print('User not authenticated')
            return False

        message = Message(chatID=chatID, senderID=current_user.id, content=messageContent, created_at=datetime.now())
        message.save()

        jsonData['createAt'] = message.created_at.strftime('%Y-%m-%d %H:%M:%S')

        print(f'User {current_user.username} sent message: ')

        emit('message', jsonData, to=chatID, broadcast=True, include_self=True)

    @socketio.on('join')
    def handle_join(jsonData):
        # Quên ép kiểu dữ liệu cho userID và chatID
        # làm tui mất 1 tiếng đồng hồ để tìm lỗi :)
        # I love Python 💖??
        userID = int(jsonData['userID'])
        room = int(jsonData['chatID'])
        join_room(room)
        emit("join", f'UserID: {userID} joined room', to=room)

    @socketio.on('leave')
    def on_leave(data):
        room = data['chatID']
        leave_room(room)

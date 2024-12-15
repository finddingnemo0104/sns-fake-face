import {io} from "socket.io-client";
import './web-components/message-element.js';

const socket = io();

class User {
    constructor(userID) {
        this.userID = userID;
    }
}

// Get elements from the DOM
const sendMessageForm = document.getElementById('send-message-form');
const messagesContainer = document.getElementById('messages-container');
const chatBtnElements = document.querySelectorAll('#chats-sidebar .list-group button');

// Add event listener to chat buttons
chatBtnElements.forEach(function (btn) {
    btn.addEventListener('click', function () {
        const chatID = btn.getAttribute('data-chat-id');
        window.location.href = '/chats?chatID=' + chatID;
    });
});

// get query parameter
const urlParams = new URLSearchParams(window.location.search);
const chatID = urlParams.get('chatID');
if (chatID) {
    const userIDInput = sendMessageForm.querySelector('input[name="userID"]');

    // Init current user
    const currentUser = new User(userIDInput.value);




    socket.on('connect', function () {
        console.log('Connected to the server');
        socket.emit('join', {userID: currentUser.userID, chatID: chatID});
    });

    socket.on("join", function (data) {
        console.log('User joined the chat:', data);
    });

    sendMessageForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const messageInput = sendMessageForm.querySelector('input[name="message"]');
        const message = messageInput.value;
        messageInput.value = '';
        socket.emit('message', {message: message, chatID: chatID, userID: currentUser.userID});
    });

    socket.on('message', function (data) {
        console.log('Received a new message:', data);
        const messageEle = document.createElement('message-element');
        messageEle.message = data.message;
        messageEle.isSender = data.userID === currentUser.userID;
        messageEle.createAt = data.createAt;
        messagesContainer.appendChild(messageEle);
        // scroll to the bottom of the messages container
        requestAnimationFrame(() => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        });
    });

}



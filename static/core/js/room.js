const roomName = JSON.parse(document.getElementById('room-name').textContent);





//websocket
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    document.querySelector('#chat-log').innerHTML += ('- ' + data.message + '<br>');
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};

function showusername() {
    const username = JSON.parse(localStorage.getItem("username"))
    document.querySelector('#user-name-box').innerHTML = ('Welcome, ' + username.username)
    console.log(username.username)
    // chatSocket.send(JSON.stringify({
    //     'username': username.username
    // }));


}
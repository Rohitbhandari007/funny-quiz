const roomName = JSON.parse(document.getElementById('room-name').textContent);

const messageaudio = document.getElementById('message-audio')
let currentuser = JSON.parse(localStorage.getItem("username"))



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


    if (data.info === 'chat') {
        document.querySelector('#chat-log').innerHTML += ('<div class="message">' + '[' + data.user + ']- ' + data.message + ' ' + '</div>');

        console.log(data.command)

        const elem = document.getElementById('chat-log')
        elem.scrollTop = elem.scrollHeight;


        if (data.user === currentuser.username) {
            console.log('i sent messege')

        } else {
            messageaudio.play()
        }
    } else {

        console.log(data.question)

        let answers = data.answer
        console.log(JSON.parse(answers))



        // answers.map = (answer) => {
        //     document.querySelector('.options').innerHTML += '<div class="option">' + answer + '</div>'
        // }
    }

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

    const user = JSON.parse(localStorage.getItem("username"))

    chatSocket.send(JSON.stringify({
        'request_type': 'chat',
        'message': message,
        'user': user.username,
        'command': 'ok'
    }))

    messageInputDom.value = '';
};

function showusername() {


    const username = JSON.parse(localStorage.getItem("username"))

    document.querySelector('#user-name-box').innerHTML = ('Welcome, ' + username.username)



}

function sendCommand() {
    chatSocket.send(JSON.stringify({
        'request_type': 'quiz',
        'newmsg': 'ok'

    }));
}
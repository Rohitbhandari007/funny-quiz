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
        document.querySelector('#chat-log').innerHTML += ('<div class="message" onclick="pickanswer()">' + '[' + data.user + ']- ' + data.message + ' ' + '</div>');

        console.log(data.command)

        const elem = document.getElementById('chat-log')
        elem.scrollTop = elem.scrollHeight;


        if (data.user === currentuser.username) {
            console.log('i sent messege')

        } else {
            messageaudio.play()
        }
    } else if (data.info === 'quiz') {


        let answers = data.answer

        let ans = JSON.parse(answers)
        let a = 0

        const options = document.querySelector('.options')

        Object.keys(ans).forEach(function (key) {
            // console.log(key, ans[key]);
            a = a + 1
            let opt = document.createElement('li')
            opt.innerHTML += a + '' + key
            opt.value += ans[key]
            options.appendChild(opt)
            // document.querySelector('.options').innerHTML += '<div class="option">' + a + ' ' + key + '</div>'

        })

        document.querySelector('.question').innerHTML = data.question

        //this function loops through childs created inside options
        for (var child = options.firstChild; child !== null; child = child.nextSibling) {
            let child_value = child.value
            child.onclick = function () {
                // 1 means true and 0 is false
                if (child_value === 1) {
                    chatSocket.send(JSON.stringify({
                        'request_type': 'answer',
                        'user_answer': 'correct',
                        'user_name': currentuser.username
                    }))
                    nextQuestion();
                } else {
                    console.log('incorrect')
                }
            };
        }




    } else if (data.info === 'answer') {
        console.log(data.message)
        console.log(data.user_name)
    } else if (data.info === 'next') {
        console.log(data.user_name)
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


function pickanswer() {
    console.log('hello')
}

function nextQuestion() {
    console.log('click')
    chatSocket.send(JSON.stringify({
        'request_type': 'next',
        'user_name': 'me'
    }))

}
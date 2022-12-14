const roomName = JSON.parse(document.getElementById('room-name').textContent);
const alertarea = document.getElementById('alert')
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

chatSocket.onopen = function (e) {
    chatSocket.send(JSON.stringify({
        'request_type': 'join',
        'username': currentuser
    }))
}

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);



    if (data.info === 'chat') {
        document.querySelector('#chat-log').innerHTML += ('<div class="message" onclick="pickanswer()">' + '[' + data.user + ']- ' + data.message + ' ' + '</div>');


        const elem = document.getElementById('chat-log')
        elem.scrollTop = elem.scrollHeight;


        if (data.user !== currentuser.username) {
            messageaudio.play()
        }
    } else if (data.info === 'quiz') {

        let answers = data.answer
        let pattern = data.pattern
        let qid = data.qid


        console.log(pattern, qid)

        localStorage.setItem("pattern", pattern)
        localStorage.setItem('qid', qid)


        let ans = JSON.parse(answers)
        let a = 0

        const options = document.querySelector('.options')
        options.innerHTML = ''

        Object.keys(ans).forEach(function (key) {
            a = a + 1
            let opt = document.createElement('li')
            opt.innerHTML += '' + key
            opt.value += ans[key]
            options.appendChild(opt)

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
                        'user_name': currentuser.username,
                    }))
                    nextQuestion();
                } else {
                    console.log('incorrect')


                }
            };
        }




    } else if (data.info === 'answer') {
        console.log(data.user_answer + ' by "' + data.user_name + '"')

    } else if (data.info === 'join_game') {

        username = data.username.username

        let message = 'Just joined'
        chatSocket.send(JSON.stringify({
            'request_type': 'chat',
            'message': message,
            'user': username,
            'command': 'ok'
        }))
    }

    else if (data.info === 'next') {

        let q_name = data.q_name
        let ans = data.answers
        let user_name = JSON.parse(data.user_name)


        let score_area = document.getElementById('score-area')

        if (user_name.username = currentuser) {
            score_area.innerHTML = user_name.username + data.points
        } else {
            let score_area2 = document.getElementById('score-area2')
            score_area2.innerHTML = user_name.username + data.points
        }






        localStorage.setItem('pattern', data.new_pattern)
        localStorage.setItem('qid', data.q_id)
        document.querySelector('.question').innerHTML = q_name


        const options = document.querySelector('.options')
        options.innerHTML = " ";


        let a = 0
        Object.keys(ans).forEach(function (key) {
            // console.log(key, ans[key]);
            a = a + 1

            let opt = document.createElement('li')
            opt.innerHTML += '' + key
            opt.value += ans[key]
            options.appendChild(opt)

        })


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
                    function alertgenerate() {
                        let errormusic = document.getElementById('error_audio')
                        errormusic.play()

                        alertarea.style.visibility = 'visible'
                    }
                    alertgenerate()
                    playErrorMusic()
                }
            };
        }




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


let points = 0

function nextQuestion() {

    points = points + 100
    points_saved = localStorage.getItem('points')


    chatSocket.send(JSON.stringify({
        'request_type': 'next',
        'user_name': localStorage.getItem('username'),
        'pattern': localStorage.getItem('pattern'),
        'qid': localStorage.getItem('qid'),
        'points': points,
    }))

}


//music 

function playErrorMusic() {
}

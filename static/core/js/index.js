var musicplaying = false;

const hoveraudio = document.getElementById('hover-audio')


function setUsername() {
    const username = document.querySelector('#user-name-input').value

    let obj = {
        'username': username
    }
    localStorage.setItem("username", JSON.stringify(obj))


    let newuserval = JSON.parse(localStorage.getItem('username'))
    console.log(newuserval)
}

function playHoverAudio() {
    hoveraudio.play()
}


function musicVolume() {
    var volumevalue = document.getElementById('slider').value
    mainmenu = document.getElementById('mainmenu-audio')
    console.log(volumevalue)
    var newvolume = volumevalue / 100;
    console.log(newvolume)
    mainmenu.volume = newvolume;

}

function playMusic() {
    mainmenu = document.getElementById('mainmenu-audio')
    mainmenu.play()
    musicplaying = true;

}

function stopMusic() {
    mainmenu = document.getElementById('mainmenu-audio')
    mainmenu.pause()
    musicplaying = false;

}

function stopErrorMusic() {
    document.getElementById('audio').pause()
}

function toggleMusic() {
    musicplaying ? stopMusic() : playMusic()
}

document.querySelector('#room-name-input').focus();
document.querySelector('#room-name-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#room-name-submit').click();
    }
};
document.querySelector('#user-name-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#room-name-submit').click();
    }
};
document.querySelector('#room-name-submit').onclick = function (e) {
    var roomName = document.querySelector('#room-name-input').value;
    const username = document.querySelector('#user-name-input').value


    if (roomName === '' | username === '') {
        console.log('room name empty');
        audio = document.getElementById("audio")
        audio.play()


        setTimeout(alertpls, 100)

        function alertpls() {
            alertarea = document.getElementById('alert')
            alertarea.style.visibility = 'visible'


        }


    } else {
        setUsername()
        window.location.pathname = '/chat/' + roomName + '/';

    }
};
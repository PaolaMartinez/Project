document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#back').onclick = () => {
       localStorage.setItem('channel', 'home')
    }

    console.log("conectado")
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    // When connected, configure buttons
    socket.on('connect', () => {

        document.querySelector('#send').onclick = () => {
            const msg_list = document.querySelector('#message_list').value;
            console.log(msg_list);
            console.log(channel)
            // document.querySelector('#message_list').value - '';
            socket.emit('send message', {'mensaje' : msg_list, 'channel': channel, 'username': localStorage.getItem('register'), 'date': new Date().toLocaleString('en-GB',  { timeZone: 'America/Guayaquil' }) });
            document.querySelector('#message_list').value = '';
        }
    });

    // When a new message is announced, add to the unordered list
    socket.on('new message', data => {
        if (data.channel == channel){
            const h3 = document.createElement('h3');
            h3.innerHTML = `${data.username} at ${data.date} : ${data.mensaje}`;
            document.querySelector('#mensajes').append(h3);
            console.log("mensaje enviado")
            var count  =  document.getElementsByTagName('h3').length;
            if (count >100){
                var tester = document.getElementById('mensajes')
                tester.removeChild(tester.childNodes[0])
            }
    }
    });
});

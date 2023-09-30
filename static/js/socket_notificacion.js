

var socket = io('http://localhost:3000')

function enviar_notificacion(data) {
    socket.emit("mi_evento", data);
}


socket.on('connect', function () {
    console.log('Conectado al servidor');

    socket.on('join', function (data) {
        console.log('Join sala', data);

    });

    socket.on('mi_evento', function (data) {
        console.log('notificacion', data);

    });
});








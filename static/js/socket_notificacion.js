

var socket = io('http://localhost:3000')

function enviar_notificacion(id) {
    socket.emit('mi_evento', id);
}   


socket.on('connect', function () {
    console.log('Conectado al servidor');

    socket.on('mi_evento', function (data) {
        console.log('Mensaje recibido del servidor:', data);

    });
    socket.on('join', function (data) {
        console.log('usuario: ', data);

    });

});









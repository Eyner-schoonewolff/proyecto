

var socket = io('http://localhost:3000')

function enviar_notificacion(data) {
    // informacion emite del froned al servidor
    socket.emit("mi_evento", data);
}

function cerrar_sala(data) {
    socket.emit("leave", data);
}

socket.on('connect', function () {
    console.log('Conectado al servidor');

    // Primero se une a la sala cuando se loguea
    socket.on('join', function (data) {
        console.log('Join sala', data);

        // luego dentro de la sala escucha la notificacion y le mando la informacion emitida
        socket.on('mi_evento', function (info) {
            // informacion que recibe del backend
            console.log('notificacion', info);

        });
        socket.on('leave', function (id) {
            console.log('sesion cerrada', id);

        });
    });

});








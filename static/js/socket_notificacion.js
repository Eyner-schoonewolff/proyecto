

var socket = io('http://localhost:3000')

function enviar_notificacion(data) {
    // informacion emite del froned al servidor
    socket.emit("mi_evento", data);
}

function cantidad_notificaiones(info) {
    // informacion emite del froned al servidor
    socket.emit("numero_notificacion", info);
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
        socket.on('mi_evento', function (servicio) {
            console.log("entro a mi evento")

            const contenedorToast = document.querySelector('#toast_notificacion');

            document.getElementById('titulo_notificacion').innerHTML = servicio.titulo;
            document.getElementById('fecha_hora_notificacion').innerHTML = servicio.horario;
            document.getElementById('contenido_notificacion').innerHTML = servicio.contenido;

            var myToast = new bootstrap.Toast(contenedorToast);

            myToast.show();

        });

        socket.on('numero_notificacion', function (numero) {
            console.log('numero de notificaciones:', numero.cantidad);
            const cantidad = document.querySelector('#numero_notificaciones')
            console.log(cantidad);
            cantidad.innerHTML = numero.cantidad;
        });

        socket.on('leave', function (id) {
            console.log('sesion cerrada', id);

        });
    });

});




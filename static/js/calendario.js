let respuesta = ''
var token = localStorage.getItem('jwt-token');


function calendario_eventos() {
    var calendarEl = document.getElementById('calendar');
    let evento = eventos();
    let arry = new Array();

    for (let index = 0; index < evento.length; index++) {
        arry.push({
            id: evento[index].id, title: evento[index].descripcion, start: evento[index].fecha, overlap: false,
            display: "background-color", color: evento[index].color, textColor: 'black', resource: evento[index].descripcion,
            allDay: false
        })
    }
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es',// especificamos el idioma español
        events: arry,

        headerToolbar: {
            left: 'prev, next, today',
            center: 'title',
            right: 'dayGridMonth',
        },

    });

    calendar.render();

}

function eventos() {
    var token = localStorage.getItem('jwt-token');
    var dato = '';

    $.ajax({
        url: 'http://localhost:3000/eventos',
        method: 'GET',
        async: false,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        success: function (datos) {
            dato = datos.eventos;
        },

    });
    return dato;
}


Promise.all([
    $.ajax({ url: '../templates/NvarContratista.html', type: 'GET', dataType: 'html' }),
    $.ajax({
        url: 'http://localhost:3000/eventos', type: 'GET', data: JSON.stringify(respuesta),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
    })
])
    .then(function (respuesta) {
        let nvarContratista = respuesta[0];
        let datos_usuario = respuesta[1];

        let nvar = document.getElementById('nvar');

        nvar.innerHTML = nvarContratista;

        let a_tipo_usuario = document.querySelector('#tipo_usuario');
        let h5_nombre_usuario = document.querySelector('#nombre_usuario');

        // Crea nodos de texto para tipo_usuario y nombre
        let tipo_usuario_texto = document.createTextNode(datos_usuario.tipo);
        let nombre_texto = document.createTextNode(datos_usuario.nombre);

        // Agrega los nodos de texto a los elementos del DOM
        a_tipo_usuario.appendChild(tipo_usuario_texto);
        h5_nombre_usuario.appendChild(nombre_texto);

        mostrar_notificacion();
        calendario_eventos();
        notificacion();
        logout();
    });
$(document).ready(function () {

    var respuesta;
    var token = localStorage.getItem('jwt-token');

    Promise.all([
        $.ajax({ url: '../templates/NvarContratista.html', type: 'GET', dataType: 'html' }),
        $.ajax({ url: '../templates/NvarCliente.html', type: 'GET', dataType: 'html' }),
        $.ajax({
            url: 'http://localhost:3000/contacto', type: 'GET', data: JSON.stringify(respuesta),
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
            let nvarCliente = respuesta[1];
            let contacto = respuesta[2];


            let nvar = document.getElementById('nvar');
            let tipo_usuario = document.getElementById('tipo_usuario');

            if (contacto.tipo == "Contratista") {
                nvar.innerHTML = nvarContratista;

                let a_tipo_usuario = document.querySelector('#tipo_usuario');
                let h5_nombre_usuario = document.querySelector('#nombre_usuario');

                // Crea nodos de texto para tipo_usuario y nombre
                let tipo_usuario_texto = document.createTextNode(contacto.tipo);
                let nombre_texto = document.createTextNode(contacto.nombre);

                // Agrega los nodos de texto a los elementos del DOM
                a_tipo_usuario.appendChild(tipo_usuario_texto);
                h5_nombre_usuario.appendChild(nombre_texto);

                document.getElementById("nombreContacto").value = contacto.nombre;
                document.getElementById("emailContacto").value = contacto.usuario.correo;
                document.getElementById("telefonoContacto").value = contacto.usuario.celular;
                
                notificacion();
                logout();
            }
            else if (contacto.tipo == "Cliente") {
                nvar.innerHTML = nvarCliente;

                let a_tipo_usuario = document.querySelector('#tipo_usuario');
                let h5_nombre_usuario = document.querySelector('#nombre_usuario');

                // Crea nodos de texto para tipo_usuario y nombre
                let tipo_usuario_texto = document.createTextNode(contacto.tipo);
                let nombre_texto = document.createTextNode(contacto.nombre);

                // Agrega los nodos de texto a los elementos del DOM
                a_tipo_usuario.appendChild(tipo_usuario_texto);
                h5_nombre_usuario.appendChild(nombre_texto);

                document.getElementById("nombreContacto").value = contacto.nombre;
                document.getElementById("emailContacto").value = contacto.usuario.correo;
                document.getElementById("telefonoContacto").value = contacto.usuario.celular;

                logout();
            }

        })

        .catch(function (error) {
            console.error('Error al cargar los archivos:', error);
        });

});



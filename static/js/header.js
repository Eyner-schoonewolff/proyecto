$(document).ready(function () {

    var respuesta;
    var token = localStorage.getItem('jwt-token');

    Promise.all([
        $.ajax({ url: '../templates/NvarContratista.html', type: 'GET', dataType: 'html' }),
        $.ajax({ url: '../templates/NvarCliente.html', type: 'GET', dataType: 'html' }),
        $.ajax({
            url: 'http://localhost:3000/header_usuarios', type: 'GET', data: JSON.stringify(respuesta),
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
            let nvar = document.getElementById('nvar');
      
            if (respuesta[2].tipo == "Contratista") {
        
                nvar.innerHTML = nvarContratista;
                let a_tipo_usuario = document.querySelector('#tipo_usuario');
                let h5_nombre_usuario = document.querySelector('#nombre_usuario');

                // Crea nodos de texto para tipo_usuario y nombre
                let tipo_usuario_texto = document.createTextNode(respuesta[2].tipo);
                let nombre_texto = document.createTextNode(respuesta[2].nombre);
             
                // Agrega los nodos de texto a los elementos del DOM
                a_tipo_usuario.appendChild(tipo_usuario_texto);
                h5_nombre_usuario.appendChild(nombre_texto);
                
                 notificacion();
                 logout();

            }
            else if (respuesta[2].tipo == "Cliente") {
                nvar.innerHTML = nvarCliente;
                let a_tipo_usuario = document.querySelector('#tipo_usuario');
                let h5_nombre_usuario = document.querySelector('#nombre_usuario');

                // Crea nodos de texto para tipo_usuario y nombre
                let tipo_usuario_texto = document.createTextNode(respuesta[2].tipo);
                let nombre_texto = document.createTextNode(respuesta[2].nombre);
             
                // Agrega los nodos de texto a los elementos del DOM
                a_tipo_usuario.appendChild(tipo_usuario_texto);
                h5_nombre_usuario.appendChild(nombre_texto);

                logout();

            }

        })

        .catch(function (error) {
            console.error('Error al cargar los archivos:', error);
        });

});



$(document).ready(function () {

    var respuesta = {};
    var token = localStorage.getItem('jwt-token');

    Promise.all([
        $.ajax({ url: '../templates/NvarContratista.html', type: 'GET', dataType: 'html' }),
        $.ajax({ url: '../templates/NvarCliente.html', type: 'GET', dataType: 'html' }),
        $.ajax({
            url: 'http://localhost:3000/actualizar', type: 'GET', data: JSON.stringify(respuesta),
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
            let datos_usuario = respuesta[2].datos[0];


            let nvar = document.getElementById('nvar');
            let tipo_usuario = document.getElementById('tipo_usuario');

            if (datos_usuario.tipo == "Contratista") {
                nvar.innerHTML = nvarContratista;

                let a_tipo_usuario = document.querySelector('#tipo_usuario');
                let h5_nombre_usuario = document.querySelector('#nombre_usuario');

                // Crea nodos de texto para tipo_usuario y nombre
                let tipo_usuario_texto = document.createTextNode(datos_usuario.tipo);
                let nombre_texto = document.createTextNode(datos_usuario.nombre);

                // Agrega los nodos de texto a los elementos del DOM
                a_tipo_usuario.appendChild(tipo_usuario_texto);
                h5_nombre_usuario.appendChild(nombre_texto);


                document.getElementById("h2_nombre").innerText = "Datos personales de " + datos_usuario.nombre;

                document.getElementById("info-nombre").value = datos_usuario.nombre;

                document.getElementById("info-email").value = datos_usuario.email;
                document.getElementById("info-documento").value = datos_usuario.numero_documento;
                document.getElementById("info-direccion").value = datos_usuario.direccion;
                document.getElementById("info-numero_celular").value = datos_usuario.numero;
                document.getElementById("info-ocupacion").value = datos_usuario.ocupacion;
                document.getElementById("info-ocupacion").value = datos_usuario.ocupacion;
                document.getElementById("descricpion_input").value = datos_usuario.descripcion;


                // modal
                document.getElementById("nombre").value = datos_usuario.nombre;
                document.getElementById("direccion").value = datos_usuario.direccion;
                document.getElementById("numeroCelular").value = datos_usuario.numero;
                document.getElementById("descripcion").value = datos_usuario.descripcion;

                // agregar ocupaciones
                let ocupaciones = datos_usuario.ocupaciones_disponibles;


                let opciones = "";
                ocupaciones.forEach((ocu) => {
                    opciones += `<option value="${ocu.id}"> ${ocu.ocupacion}</option>`
                });

                $("#agregar_ocupacion").append(opciones);

            }
            else if (datos_usuario.tipo == "Cliente") {
                nvar.innerHTML = nvarCliente;

                let a_tipo_usuario = document.querySelector('#tipo_usuario');
                let h5_nombre_usuario = document.querySelector('#nombre_usuario');

                // Crea nodos de texto para tipo_usuario y nombre
                let tipo_usuario_texto = document.createTextNode(datos_usuario.tipo);
                let nombre_texto = document.createTextNode(datos_usuario.nombre);

                // Agrega los nodos de texto a los elementos del DOM
                a_tipo_usuario.appendChild(tipo_usuario_texto);
                h5_nombre_usuario.appendChild(nombre_texto);

                document.getElementById("h2_nombre").innerText = "Datos personales de " + datos_usuario.nombre;

                document.getElementById("info-nombre").value = datos_usuario.nombre;

                document.getElementById("info-email").value = datos_usuario.email;
                document.getElementById("info-documento").value = datos_usuario.numero_documento;
                document.getElementById("info-direccion").value = datos_usuario.direccion;
                document.getElementById("info-numero_celular").value = datos_usuario.numero;
                document.getElementById("info-ocupacion").value = datos_usuario.ocupacion;
                document.getElementById("info-ocupacion").value = datos_usuario.ocupacion;
                document.getElementById("descricpion_input").value = datos_usuario.descripcion;
             

            }

        })

        .catch(function (error) {
            console.error('Error al cargar los archivos:', error);
        });

});



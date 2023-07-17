$(document).ready(function () {

    var respuesta = {};
    var token = localStorage.getItem('jwt-token');

    Promise.all([
        $.ajax({ url: '../templates/NvarContratista.html', type: 'GET', dataType: 'html' }),
        $.ajax({ url: '../templates/NvarCliente.html', type: 'GET', dataType: 'html' }),
        $.ajax({
            url: 'http://localhost:3000/perfiles', type: 'GET', data: JSON.stringify(respuesta),
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
            let perfil = respuesta[2];

            let nvar = document.getElementById('nvar');
            let tipo_usuario = document.getElementById('tipo_usuario');

            if (perfil.tipo == "Contratista") {
                nvar.innerHTML = nvarContratista;

                let a_tipo_usuario = document.querySelector('#tipo_usuario');
                let h5_nombre_usuario = document.querySelector('#nombre_usuario');

                // Crea nodos de texto para tipo_usuario y nombre
                let tipo_usuario_texto = document.createTextNode(perfil.tipo);
                let nombre_texto = document.createTextNode(perfil.nombre);
                let texto_tipo = document.createTextNode('Cliente');

                // Agrega los nodos de texto a los elementos del DOM
                a_tipo_usuario.appendChild(tipo_usuario_texto);
                h5_nombre_usuario.appendChild(nombre_texto);
                tipo_usuario.appendChild(texto_tipo);

                if (perfil.perfiles_usuario.length > 0) {
                    // const perfilesContainer = document.getElementById("perfilesContainer");
                    perfil.perfiles_usuario.forEach(perfil => {
                        let html = "";
                        html += `<div class="col-lg-4">
                        <div class="card mb-5">
                            <div class="card-body">
                                <h5 class="card-title">${perfil.nombre}</h5>
                                <a onclick="addClickEventToButtons()" class="btn btn-success btn-sm bi bi-eye-fill btn-perfil" title="Ver calificacion">
                                    Calificacion</a>
                                <input class="id_perfil" name="idPerfil" type="hidden" value=${perfil.id}>
                            </div>
                            <div class="card-footer text-muted">
                                ${perfil.dia_calificacion}
                            </div>
                        </div>
                    </div>`

                        $("#perfilesContainer").append(html);
                    });


                } else {
                    let perfil_vacio = document.querySelector('#perfil_vacio')
                    perfil_vacio.innerHTML = `
                    <div class="d-flex justify-content-center align-items-center" style="height: 100vh;">
                      <h4 class="text-center">No hay perfiles para mostrar</h4>
                    </div>
                  `;
                }

            } else if (perfil.tipo == "Cliente") {

                nvar.innerHTML = nvarCliente;
                let a_tipo_usuario = document.querySelector('#tipo_usuario');
                let h5_nombre_usuario = document.querySelector('#nombre_usuario');

                // Crea nodos de texto para tipo_usuario y nombre
                let tipo_usuario_texto = document.createTextNode(perfil.tipo);
                let nombre_texto = document.createTextNode(perfil.nombre);
                let texto_tipo = document.createTextNode('Contratista');

                // Agrega los nodos de texto a los elementos del DOM
                a_tipo_usuario.appendChild(tipo_usuario_texto);
                h5_nombre_usuario.appendChild(nombre_texto);
                tipo_usuario.appendChild(texto_tipo);


                if (perfil.perfiles_usuario.length > 0) {

                    perfil.perfiles_usuario.forEach(perfil => {
                        let html = "";
                        html += `<div class="col-lg-4">
                        <div class="card mb-5">
                            <div class="card-body">
                                <h5 class="card-title">${perfil.nombre}</h5>
                                <a onclick="addClickEventToButtons()" class="btn btn-success btn-sm bi bi-eye-fill btn-perfil" title="Ver calificacion">
                                    Calificacion</a>
                                <input class="id_perfil" name="idPerfil" type="hidden" value=${perfil.id}>
                            </div>
                            <div class="card-footer text-muted">
                                ${perfil.dia_calificacion}
                            </div>
                        </div>
                    </div>`

                        $("#perfilesContainer").append(html);
                    });

                } else {
                    let perfil_vacio = document.querySelector('#perfil_vacio')
                    perfil_vacio.innerHTML = `
                    <div class="d-flex justify-content-center align-items-center" style="height: 100vh;">
                      <h4 class="text-center">No hay perfiles para mostrar</h4>
                    </div>
                  `;
                }

            }
            // const contenido = document.getElementById('contenido');
            // contenido.innerHTML = paginaHomeResponse;

            // const nvar = document.getElementById('nvar');
            // nvar.innerHTML = nvarResponse;
        })
        .catch(function (error) {
            console.error('Error al cargar los archivos:', error);
        });

});



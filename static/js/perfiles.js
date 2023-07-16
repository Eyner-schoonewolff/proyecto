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
                    const perfilesContainer = document.getElementById("perfilesContainer");

                    // Recorre el array de perfiles
                    perfil.perfiles_usuario.forEach(perfil => {
                        // Crea los elementos HTML correspondientes
                        const divCol = document.createElement("div");
                        divCol.className = "col-lg-4";

                        const divCard = document.createElement("div");
                        divCard.className = "card mb-5";

                        const divCardBody = document.createElement("div");
                        divCardBody.className = "card-body";

                        const cardTitle = document.createElement("h5");
                        cardTitle.className = "card-title";
                        cardTitle.textContent = perfil.nombre;

                        const btnCalificacion = document.createElement("a");
                        btnCalificacion.href = "perfiles/"+ perfil.id;
                        btnCalificacion.className = "btn btn-success btn-sm bi bi-eye-fill btn-perfil";
                        btnCalificacion.title = "Ver calificacion";
                        btnCalificacion.textContent = "Calificacion";
                        // Agrega el enlace correspondiente si tienes una URL para ver la calificación

                        const idPerfilInput = document.createElement("input");
                        idPerfilInput.className = "id_perfil";
                        idPerfilInput.name = "idPerfil";
                        idPerfilInput.type = "hidden";
                        idPerfilInput.value = perfil.id;

                        const div_card = document.createElement("div");
                        div_card.className = "card-footer text-muted ";
                        div_card.style.display = "block"; // Hacer que el elemento ocupe todo el ancho
                        div_card.style.marginTop = "20px"; // Ajustar el margen superior según tus necesidades
                        div_card.style.marginBottom = "15px";
                        div_card.innerText = perfil.dia_calificacion;


                        // Agrega los elementos al DOM en la estructura adecuada
                        divCardBody.appendChild(cardTitle);
                        divCardBody.appendChild(btnCalificacion);
                        divCardBody.appendChild(div_card);
                        divCardBody.appendChild(idPerfilInput);

                        divCard.appendChild(divCardBody);
                        divCol.appendChild(divCard);

                        // Agrega el perfil al contenedor
                        perfilesContainer.querySelector(".row").appendChild(divCol);

                        // let card_footer=querySelector.getElementById('card_footer');
                        // card_footer.innerHTML=perfil.dia_calificacion;
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
                    const perfilesContainer = document.getElementById("perfilesContainer");

                    // Recorre el array de perfiles
                    perfil.perfiles_usuario.forEach(perfil => {
                        // Crea los elementos HTML correspondientes
                        const divCol = document.createElement("div");
                        divCol.className = "col-lg-4";

                        const divCard = document.createElement("div");
                        divCard.className = "card mb-5";

                        const divCardBody = document.createElement("div");
                        divCardBody.className = "card-body";

                        const cardTitle = document.createElement("h5");
                        cardTitle.className = "card-title";
                        cardTitle.textContent = perfil.nombre;

                        const btnCalificacion = document.createElement("a");
                        btnCalificacion.href="perfiles/" + perfil.id;
                        btnCalificacion.className = "btn btn-success btn-sm bi bi-eye-fill btn-perfil";
                        btnCalificacion.title = "Ver calificacion";
                        btnCalificacion.textContent = "Calificacion";
                        // Agrega el enlace correspondiente si tienes una URL para ver la calificación
                        // btnCalificacion.href = ...;

                        const idPerfilInput = document.createElement("input");
                        idPerfilInput.className = "id_perfil";
                        idPerfilInput.name = "idPerfil";
                        idPerfilInput.type = "hidden";
                        idPerfilInput.value = perfil.id;

                        const div_card = document.createElement("div");
                        div_card.className = "card-footer text-muted ";
                        div_card.style.display = "block"; // Hacer que el elemento ocupe todo el ancho
                        div_card.style.marginTop = "20px"; // Ajustar el margen superior según tus necesidades
                        div_card.style.marginBottom = "15px";
                        div_card.innerText = perfil.dia_calificacion;


                        // Agrega los elementos al DOM en la estructura adecuada
                        divCardBody.appendChild(cardTitle);
                        divCardBody.appendChild(btnCalificacion);
                        divCardBody.appendChild(div_card);
                        divCardBody.appendChild(idPerfilInput);

                        divCard.appendChild(divCardBody);
                        divCol.appendChild(divCard);

                        // Agrega el perfil al contenedor
                        perfilesContainer.querySelector(".row").appendChild(divCol);

                        // let card_footer=querySelector.getElementById('card_footer');
                        // card_footer.innerHTML=perfil.dia_calificacion;
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



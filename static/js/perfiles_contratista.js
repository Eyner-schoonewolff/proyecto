function agregar() {
    var respuesta;
    var token = localStorage.getItem('jwt-token');

    Promise.all([
        $.ajax({ url: '../templates/NvarCliente.html', type: 'GET', dataType: 'html' }),
        $.ajax({
            url: 'http://localhost:3000/contratistas', type: 'GET', data: JSON.stringify(respuesta),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            }
        })
    ]).then(function (respuesta) {
        let nvarCliente = respuesta[0];
        let datos = respuesta[1];
        let datos_contratista=respuesta[1].perfiles;
        let nvar = document.getElementById('nvar');
        nvar.innerHTML = nvarCliente;

        let a_tipo_usuario = document.querySelector('#tipo_usuario');
        let h5_nombre_usuario = document.querySelector('#nombre_usuario');

        // Crea nodos de texto para tipo_usuario y nombre
        let tipo_usuario_texto = document.createTextNode(datos.tipo);
        let nombre_texto = document.createTextNode(datos.nombre);

        // Agrega los nodos de texto a los elementos del DOM
        a_tipo_usuario.appendChild(tipo_usuario_texto);
        h5_nombre_usuario.appendChild(nombre_texto);

        let con=1;
        let html="";
        $.each(datos_contratista, function (i, item) {
            html += `<div class="mx-5 py-3 ">
            <div class="slide-container swiper">
                <div class="slide-content">
                    <div class="card-wrapper swiper-wrapper">
                    
                        <div class="card swiper-slide mb-5">
                            <div class="image-content">
                                <span class="overlay"></span>
                                <div class="card-image">
                                    <img src="../static/imagen/perfiles.png" id="img">
                                </div>
                            </div>
                            <div class="card-body">
                                <h2>Contratista ${con}</h2>
                                <p class="card-text">
                                ${item.nombre_completo}
                                </p>
                                <p class="card-text">
                                    <b>Telefono:</b> ${item.celular}<br>
                                    <b>Correo:</b> ${item.email}<br>
                                    <b>Ocupaciones:</b> ${item.ocupaciones}.
                                </p>
                            </div>


                        </div>
                    </div>
                </div>
            </div>
            </div>`;
            con++;
        })

        $("#container_div").append(html);
        logout();

    });
}


agregar()
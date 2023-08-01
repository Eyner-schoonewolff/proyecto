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

                // agregar ocupaciones
                let ocupaciones = datos_usuario.ocupaciones_disponibles;
                let html = ""

                html += `<div class="row ">
                <div class="col-lg-12 d-flex justify-content-center">
                    <div class="col-lg-6 card shadow-lg" style="margin: 0 9px 0 0;">
                        <div class="card-body p-5">
                            <div class="row">
                                <div class="col-lg-12">
                                    <div id="formulario" class="mb-4 m-2">
                                        <h2 id="h2_nombre" class="fw-bold mb-5"></h2>

                                        <div class="form-outline mb-5">

                                            <div class="row">

                                                <div class="col-6 mb-2">
                                                    <label class="form-label m-2" for="form3Example3">Nombre
                                                        completo</label>
                                                    <input id="info-nombre" type="text" name="nombre" class="form-control"
                                                        value="" readonly />

                                                </div>

                                                <div class="col-6 mb-2">
                                                    <label for="email" class="m-2">Email</label>
                                                    <input id="info-email" type="email" class="form-control" name="email"
                                                        value="" placeholder="" readonly>
                                                </div>


                                            </div>
                                            <div class="row">
                                                <div class="col mb-2">
                                                    <label class="form-label" for="form3Example3">Numero de
                                                        documento</label>
                                                    <input id="info-documento" type="number" name="documento" min="4" max="12"
                                                        class="form-control" value="" readonly />

                                                </div>


                                                <div class="col mb-2">
                                                    <label class="form-label" for="form3Example3">Dirección</label>
                                                    <input id="info-direccion" type="text" name="direccion" class="form-control"
                                                        value="" readonly />

                                                </div>


                                            </div>
                                            <div class="row">
                                                <div class="col-6 mb-2">
                                                    <label class="form-label" for="form3Example3">Celular</label>
                                                    <input id="info-numero_celular" type="number" name="numeroCelular" min="4" max="12"
                                                        class="form-control" value="" readonly />

                                                </div>

                                                <div class="col-6 mb-2">
                                                    <label class="form-label" for="form3Example3">
                                                        Ocupaciones</label>
                                                    <input id="info-ocupacion" type="text" name="nombre_ocupaciones" class="form-control"
                                                        value="" readonly />
                                                </div>

                                            </div>
                                            <div class="row">
                                                <div class="col-12 mb-2">
                                                    <label class="form-label" for="form3Example3">Descripcion 
                                                        Contratista</label>
                                                    <input id="descricpion_input" type="text" name="descricpion_input"
                                                       class="form-control" value="" readonly />

                                                </div>
                                            </div>

                                        </div>
                                        <div class="mb-4 row justify-content-center">
                                            <button type="button" class="btn btn-warning" data-bs-toggle="modal"
                                                data-bs-target="#exampleModal">
                                                <i class="bi bi-pencil-square"></i>
                                                Actualizar
                                            </button>
                                        </div>

                                        <div class="modal fade " data-bs-backdrop="static" data-bs-keyboard="false"
                                            tabindex="-1" id="exampleModal" aria-labelledby="exampleModalLabel"
                                            aria-hidden="true">
                                            <div class="modal-dialog modal-lg modal-dialog-centered">
                                                <div class="modal-content">
                                                    <div class="modal-header">
                                                        <h5 class="modal-title" id="exampleModalLabel">Actualizar
                                                        </h5>
                                                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                                                            aria-label="Close"></button>
                                                    </div>
                                                    <div class="modal-body">
                                                        <div class="form-outline mb-5">
                                                            <div class="row">
                                                                <div class="col-6 mb-2">
                                                                    <label class="form-label m-2"
                                                                        for="form3Example3">Nombre
                                                                        completo</label>
                                                                    <input id="nombre" type="text" name="nombre"
                                                                        class="form-control" value="" />
                                                                </div>
                                                                <div class="col-6 mb-2">
                                                                    <label class="form-label m-2"
                                                                        for="form3Example3">Dirección</label>
                                                                    <input id="direccion" type="text" name="direccion"
                                                                        class="form-control" value="" />
                                                                </div>

                                                            </div>
                                                            <div class="row">
                                                                <div class="col-6 mb-2">
                                                                    <label class="form-label m-2"
                                                                        for="form3Example3">Celular</label>
                                                                    <input id="numeroCelular" type="number"
                                                                        name="numeroCelular" min="4" max="12"
                                                                        class="form-control" value="" />

                                                                </div>
                                                                <div class="col-6 mb-2">
                                                                    <label class="form-label m-2"
                                                                        for="form3Example3">Descripcion</label>
                                                                    <input id="descripcion" type="text" name="descripcion"
                                                                        class="form-control" value="" />
                                                                </div>

                                                            </div>

                                                        </div>
                                                    </div>
                                                    <div class="modal-footer">
                                                        <button type="button" id="btn-actuzalizar"
                                                            class="btn btn-success">
                                                            Guardar</button>
                                                        <button type="button" class="btn btn-secondary"
                                                            data-bs-dismiss="modal">Cerrar</button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>

                    <div class="col-lg-6 card shadow-lg">
                        <div class="card-body p-5">
                            <div class="row">
                                <div class="col-lg-12">
                                    <h1>Agregar Ocupaciones</h1>
                                    <div class="col-6 mt-5 text-center" style="margin: auto; text-align: center;">
                                        <select id="agregar_ocupacion" multiple name="ocupacion"
                                            class="form-control mb-3">
                                        </select>
                                    </div><br>
                                    <a id="btn-agregar-ocupacion" class="btn btn-primary" role="button"
                                        data-mdb-toggle="button" onclick="actualizar_ocu()">Actualizar ocupacion</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                        </div>`

                
                $("#contenedor-pagina").append(html);

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

                let opciones = "";
                ocupaciones.forEach((ocu) => {
                    opciones += `<option value="${ocu.id}"> ${ocu.ocupacion}</option>`
                });

                $("#agregar_ocupacion").append(opciones);

                actuzalizar();
                mostrar_ocupaciones();

            }
            else if (datos_usuario.tipo == "Cliente") {
                let html = "";
                nvar.innerHTML = nvarCliente;

                let a_tipo_usuario = document.querySelector('#tipo_usuario');
                let h5_nombre_usuario = document.querySelector('#nombre_usuario');

                // Crea nodos de texto para tipo_usuario y nombre
                let tipo_usuario_texto = document.createTextNode(datos_usuario.tipo);
                let nombre_texto = document.createTextNode(datos_usuario.nombre);

                // Agrega los nodos de texto a los elementos del DOM
                a_tipo_usuario.appendChild(tipo_usuario_texto);
                h5_nombre_usuario.appendChild(nombre_texto);


                html += `<section class="h-100 text-center">
                <div class="container mt-5 h-100">
                    <div class="row justify-content-sm-center h-100">
                        <div class="col-xxl-7 col-xl-5 col-lg-7 col-md-9 col-sm-9">
                            <div class="card shadow-lg">
                                <div class="card-body p-5">
                                    <div class="row d-flex justify-content-center">
                                        <div class="col-lg-12">
                                            <div id="formulario" class="mb-4 m-2">
                                                <h2 class="fw-bold mb-5">Datos personales de ${datos_usuario.nombre}</h2>
        
                                                <div class="form-outline mb-5">
                                                    <div class="row">
                                                        <div class="col-6 mb-2">
                                                            <label class="form-label m-2" for="form3Example3">Nombre
                                                                completo</label>
                                                            <input type="text" name="nombre" class="form-control text-center"
                                                                value="${datos_usuario.nombre}" readonly />
                                                        </div>
        
                                                        <div class="col-6 mb-2">
                                                            <label for="email" class="m-2">Email</label>
                                                            <input type="email" class="form-control text-center" name="email"
                                                                placeholder="" value="${datos_usuario.email}" readonly>
                                                        </div>
        
        
                                                    </div>
                                                    <div class="row">
                                                        <div class="col mb-2">
                                                            <label class="form-label" for="form3Example3">Numero de
                                                                documento</label>
                                                            <input type="number" name="documento" min="4" max="12"
                                                                class="form-control text-center" value="${datos_usuario.numero_documento}"
                                                                readonly />
                                                        </div>
        
        
                                                        <div class="col mb-2">
                                                            <label class="form-label" for="form3Example3">Dirección</label>
                                                            <input type="text" name="direccion" class="form-control"
                                                                value="${datos_usuario.direccion}" readonly />
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-12 mb-2">
                                                            <label class="form-label" for="form3Example3">Numero de
                                                                Celular</label>
                                                            <input type="number" name="documento" min="4" max="12"
                                                                class="form-control text-center" value="${datos_usuario.numero}" readonly />
        
                                                        </div>
                                                    </div>
                                                </div>
        
                                                <div class="mb-4 row justify-content-center">
                                                    <button type="button" class="btn btn-warning" data-bs-toggle="modal"
                                                        data-bs-target="#exampleModal">
                                                        <i class="bi bi-pencil-square"></i>
                                                        Actualizar
                                                    </button>
                                                </div>
        
                                                <div class="modal fade " data-bs-backdrop="static" data-bs-keyboard="false"
                                                    tabindex="-1" id="exampleModal" aria-labelledby="exampleModalLabel"
                                                    aria-hidden="true">
                                                    <div class="modal-dialog modal-lg modal-dialog-centered">
                                                        <div class="modal-content">
                                                            <div class="modal-header">
                                                                <h5 class="modal-title" id="exampleModalLabel">Actualizar
                                                                </h5>
                                                                <button type="button" class="btn-close" data-bs-dismiss="modal"
                                                                    aria-label="Close"></button>
                                                            </div>
                                                            <div class="modal-body">
                                                                <div class="form-outline mb-5">
                                                                    <div class="row">
                                                                        <div class="col-6 mb-2">
                                                                            <label class="form-label m-2"
                                                                                for="form3Example3">Nombre
                                                                                completo</label>
                                                                            <input id="nombre" type="text" name="nombre"
                                                                                class="form-control text-center"
                                                                                value="${datos_usuario.nombre}"/>
                                                                        </div>
        
                                                                        <div class="col-6 mb-2">
                                                                            <label class="form-label m-2"
                                                                                for="form3Example3">Dirección</label>
                                                                            <input id="direccion" type="text" name="direccion"
                                                                                class="form-control text-center"
                                                                                value="${datos_usuario.direccion}" />
                                                                        </div>
        
                                                                    </div>
                                                                    <div class="row">
                                                                        <div class="col-12 mb-2">
                                                                            <label class="form-label" for="form3Example3">Numero
                                                                                de
                                                                                Celular</label>
                                                                            <input id="numeroCelular" type="number"
                                                                                name="numeroCelular" min="4" max="12"
                                                                                class="form-control text-center"
                                                                                value="${datos_usuario.numero}" />
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="modal-footer">
                                                                <button type="button" id="btn-actuzalizar"
                                                                    class="btn btn-success">
                                                                    Guardar</button>
                                                                <button type="button" class="btn btn-secondary"
                                                                    data-bs-dismiss="modal">Cerrar</button>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                </div>
                    </section>`

                $("#contenedor-pagina").append(html);

            }
            actuzalizar();

        })

        .catch(function (error) {
            console.error('Error al cargar los archivos:', error);
        });

});



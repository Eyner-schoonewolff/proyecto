$(document).ready(function () {

    var respuesta = "";
    var token = localStorage.getItem('jwt-token');

    Promise.all([
        $.ajax({ url: '../templates/NvarContratista.html', type: 'GET', dataType: 'html' }),
        $.ajax({ url: '../templates/NvarCliente.html', type: 'GET', dataType: 'html' }),
        $.ajax({
            url: 'http://localhost:3000/consultar', type: 'GET', data: JSON.stringify(respuesta),
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
            let trabajos = respuesta[2];

            let nvar = document.getElementById('nvar');

            let table;
            table = document.querySelector('#paginacion_usuarios');

            if (trabajos.tipo == "Contratista") {
                nvar.innerHTML = nvarContratista;
                // notificacion();
                let a_tipo_usuario = document.querySelector('#tipo_usuario');
                let h5_nombre_usuario = document.querySelector('#nombre_usuario');

                // Crea nodos de texto para tipo_usuario y nombre
                let tipo_usuario_texto = document.createTextNode(trabajos.tipo);
                let nombre_texto = document.createTextNode(trabajos.nombre);

                // Agrega los nodos de texto a los elementos del DOM
                a_tipo_usuario.appendChild(tipo_usuario_texto);
                h5_nombre_usuario.appendChild(nombre_texto);
                const objeto = JSON.parse(trabajos.consulta_contratista)
                $(document).ready(function () {
                    let cabecera = "";
                    cabecera += `<tr>
                        <th scope="col">Nombre</th>
                        <th scope="col">Celular</th>
                        <th scope="col" class="fecha"> Fecha</th>
                        <th scope="col">Direccion</th>
                        <th scope="col">Estado</th>
                        <th scope="col">Funciones</th>
                  </tr>`
                    $("#cabecera").append(cabecera);
                    objeto.forEach((consulta) => {
                        let html = "";
                        let modal = "";
                        html += `
                        <tr>
                          <td scope="row">${consulta.nombre}</td>
                          <td>${consulta.numero}</td>
                          <td>${consulta.horario}</td>
                          <td>${consulta.direccion}</td>
                          <td>${consulta.estado}</td>
                          <td class="mt-2">
                            ${consulta.estado === "Finalizada" || consulta.estado === "Cancelada"
                                ? `<a class="btn btn-secondary bi bi-arrow-clockwise m-1" title="desactivado"></a>`
                                : `<a id="guardar-id-${consulta.id}" class="btn btn-warning bi bi-arrow-clockwise m-1" title="actualizar estado"></a>`
                            }
                            <a type="button" id="${consulta.id}" class="btn btn-info bi bi-eye-fill"></a>
                          </td>
                        </tr>
                      `;

                        modal += `
                    <div class="modal fade" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
                          id="exampleModal-${consulta.id}" aria-labelledby="exampleModalLabel-${consulta.id}" aria-hidden="true">
                        <div class="modal-dialog modal-lg modal-dialog-centered">
                          <div class="modal-content">
                            <div class="modal-header">
                              <h5 class="modal-title" id="exampleModalLabel">Actualizar Estado</h5>
                              <button type="button" class="btn-close" data-bs-dismiss="modal"
                                aria-label="Close"></button>
                            </div>
                                <div class="modal-body">
                                    <div class="form-outline mb-5">
                                        <div class="row mt-3">
                                            <div class="col-12 mb-2">
                                                <label for="estado" class="m-2">Estado actual</label>
                                                ${consulta.estado === 'Aceptada' ? `

                                                <h3 id="estado_actual" style="color:green;" class="mt-2 text-center">${consulta.estado}</h3>
                                                <input id="id_consulta" name="prodId" type="hidden" value=${consulta.id}>

                                                `: consulta.estado === 'Pendiente' ? `
                                                <h3 id="estado_actual" style="color:darkblue;" class="mt-2 text-center">${consulta.estado}</h3>
                                                <input id="id_consulta" name="prodId" type="hidden" value=${consulta.id}>
                                                `

                                                 : consulta.estado == 'Finalizada' ? `
                                                <h3 id="estado_actual" style="color:red;" class="mt-2 text-center">${consulta.estado}</h3>
                                                <input id="id_consulta" name="prodId" type="hidden" value=${consulta.id}>
                                                `

                                    : ''}
                                                 
                                            </div>
                                         </div>
                                
                                            ${consulta.estado === "Pendiente" ? `
                                        <div class="row">
                                            <div class="col mb-2">
                                                <label for="fecha_actual" class="m-2">Fecha de Solicitud</label>
                                                <input id="fecha_actual" type="text" class="form-control text-center" name="fecha_actual" value="${consulta.horario}" readonly>
                                            </div>
                                            <div class="col mb-2">
                                                <label for="tiempo" class="m-2">Fecha a actualizar</label>
                                                <input type="date" class="form-control text-center" id="fecha_actualizar" name="fecha">
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col mb-2">
                                                <label for="hora_actual" class="m-2">Hora de Solicitud</label>
                                                <input id="hora_actual" type="text" class="form-control text-center" name="hora_actual" value="${consulta.hora}" readonly>
                                            </div>
                                            <div class="col mb-2">
                                                <label for="tiempo" class="m-2">Hora a actualizar</label>
                                                <input type="time" class="form-control text-center" id="hora_actualizar" name="hora" step="1">
                                            </div>
                                        </div>
                                    ` : ''}
                                    <div class="row mt-3">
                                        <div class="col-12 mb-2">
                                            <label for="select" class="m-3">Cambiar estado</label>
                                            <select class="form-select text-center" aria-label="Default select example" id="select_estado">
                                                ${consulta.estado === "Pendiente" ?
                                `<option value="2">Aceptar</option>
                                                    <option value="3">Cancelar</option>` :
                                consulta.estado === "Aceptada" ?
                                    `<option value="4">Finalizar</option>` :
                                    ''}
                                            </select>
                                        </div>
                                    </div>
                                    </div>
                                    <div class="modal-footer">
                                    <a onclick="guardar_estado()" id="btn-guardar-estado" class="btn btn-success">Guardar</a>
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                                </div>
                                </div>
                                </div>
                                </div>
                                </div>
                            `;

                        $("#consultar").append(html);
                        $("#modal").append(modal);


                        const btnAbrirModal = document.getElementById(`guardar-id-${consulta.id}`);

                        if (btnAbrirModal) {
                            btnAbrirModal.addEventListener("click", function () {
                                setTimeout(function () {
                                    let modalElement = document.querySelector(`#exampleModal-${consulta.id}`);
                                    const modalInstance = new bootstrap.Modal(modalElement);
                                    modalInstance.show();
                                }, 100);
                            });
                        }
                    });
                    if (table) {
                        paginacion_datatable();
                    }

                    $(function () {

                        $(document).on('click', 'a[type="button"]', function () {
                            let id = this.id;
                            console.log(id);

                            $.ajax({
                                url: 'http://localhost:3000/evidencia/' + id,
                                type: 'GET',
                                // data: JSON.stringify(id),
                                contentType: 'application/json; charset=utf-8',
                                dataType: 'json',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'Authorization': 'Bearer ' + token
                                },
                                success: function (respuesta) {
                                    let imagenURL = 'http://localhost:3000/static/img/' + respuesta.informacion.evidencia;
                                    let descripcion = respuesta.informacion.descripcion;

                                    let parametrosURL = '?imagenURL=' + encodeURIComponent(imagenURL) + '&descripcion=' + encodeURIComponent(descripcion);

                                    // Redirigir a la nueva página con los parámetros en la URL
                                    window.location.href = '/templates/evidencias.html' + parametrosURL;
                                },
                                error: function (error) {
                                    console.log(error);
                                }
                            });
                        });

                    });
                });


                notificacion();
                logout();
            }

            else if (trabajos.tipo == "Cliente") {
                nvar.innerHTML = nvarCliente;
                let a_tipo_usuario = document.querySelector('#tipo_usuario');
                let h5_nombre_usuario = document.querySelector('#nombre_usuario');

                // Crea nodos de texto para tipo_usuario y nombre
                let tipo_usuario_texto = document.createTextNode(trabajos.tipo);
                let nombre_texto = document.createTextNode(trabajos.nombre);

                // Agrega los nodos de texto a los elementos del DOM
                a_tipo_usuario.appendChild(tipo_usuario_texto);
                h5_nombre_usuario.appendChild(nombre_texto);
                const objeto = JSON.parse(trabajos.consultar_cliente);
                $(document).ready(function () {
                    let cabecera = "";
                    cabecera += `<tr>
                    <th scope="col">Nombre</th>
                    <th scope="col">Celular</th>
                    <th scope="col" class="fecha"> Fecha</th>
                    <th scope="col">Ocupacion</th>
                    <th scope="col">Estado</th>
                    <th scope="col">Funciones</th>
                 </tr>`
                    $("#cabecera").append(cabecera);
                    objeto.forEach((consulta) => {
                        let html = "";

                        html += `
                        <tr>
                          <td scope="row">${consulta.nombre}</td>
                          <td>${consulta.numero}</td>
                          <td>${consulta.horario}</td>
                          <td>${consulta.ocupacion}</td>
                          <td>${consulta.estado}</td>
                          <td class="mt-2">
                            ${consulta.estado === "Aceptada" || consulta.estado === "Cancelada"
                                ? `<a class="btn btn-secondary"> <i class="bi bi-trash3"></i></a>`
                                : ` <a type="button" id="${consulta.id}" class="btn btn-danger "><i
                                class="bi bi-trash3">`
                            }
                          </td>
                        </tr>
                      `;

                        $("#consultar").append(html);



                    });
                });

                paginacion_datatable();

                $(function () {
                    $(document).on('click', 'a[type="button"]', function (event) {
                        let id = this.id;
                        var confirmar_respuesta = new Boolean(false);

                        Swal.fire({
                            title: '¿Estas seguro de cancelar su solicitud?',
                            text: "¡No podrás revertir esto!",
                            icon: 'warning',
                            showCancelButton: true,
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'Si, deseo cancelar!'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                confirmar_respuesta.value = result.isConfirmed

                            } else {
                                confirmar_respuesta.value = result.isConfirmed;
                            }

                            $.ajax({
                                url: 'http://localhost:3000/cancelar', type: 'POST', data: JSON.stringify({
                                    'id': id,
                                    'confirmacion': confirmar_respuesta.value
                                }),
                                contentType: 'application/json; charset=utf-8',
                                dataType: 'json',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'Authorization': 'Bearer ' + token
                                },
                                success: function (respuesta) {
                                    if (respuesta.confirmar) {
                                        Swal.fire(
                                            'Solicitud cancelada!',
                                            'Se ha cancelado con exito.',
                                            'success'
                                        ).then(() => {
                                            window.location.href = respuesta.recargar;
                                        });
                                    } else {
                                        return;
                                    }
                                },
                                error: function (error) {
                                    console.log(error);
                                }
                            });
                        });

                    });
                });

                logout();
            }

        })

        .catch(function (error) {
            console.error('Error al cargar los archivos:', error);
        });

});




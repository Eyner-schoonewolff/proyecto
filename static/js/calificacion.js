
$(document).ready(function () {

    var respuesta = {};
    var token = localStorage.getItem('jwt-token');

    Promise.all([
        $.ajax({ url: '../templates/NvarContratista.html', type: 'GET', dataType: 'html' }),
        $.ajax({ url: '../templates/NvarCliente.html', type: 'GET', dataType: 'html' }),
        $.ajax({
            url: 'http://localhost:3000/calificar', type: 'GET', data: JSON.stringify(respuesta),
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
            let calificar = respuesta[2];

            let consultas=""
            let nvar = document.getElementById('nvar');
            let h2_texto_calificar=document.querySelector('#calificar')
            

            if (calificar.tipo == "Contratista") {
                consultas=calificar.consulta_contratista;
                nvar.innerHTML = nvarContratista;
                
                h2_texto_calificar.innerHTML='Calificar Clientes'
                let a_tipo_usuario = document.querySelector('#tipo_usuario');
                let h5_nombre_usuario = document.querySelector('#nombre_usuario');

                // Crea nodos de texto para tipo_usuario y nombre
                let tipo_usuario_texto = document.createTextNode(calificar.tipo);
                let nombre_texto = document.createTextNode(calificar.nombre);

                // Agrega los nodos de texto a los elementos del DOM
                a_tipo_usuario.appendChild(tipo_usuario_texto);
                h5_nombre_usuario.appendChild(nombre_texto);

                const objetos = JSON.parse(consultas);
                $(document).ready(function () {
                    objetos.forEach((consulta) => {
                        let html = "";
                        let modal = "";
                        html += `
                        <tr>
                        ${consulta.estado === "Finalizada"
                                ? `<tr id="fila-${consulta.id}">
                            <td scope="row">${consulta.nombre} <a style="font-size: 1.3em;"
                                    class="bi bi-person-circle m-2 "
                                    data-id="${consulta.id}"></a> </td>
                            <td>${consulta.numero}</td>
                            <td>${consulta.horario}</td>
                            <td>${consulta.direccion}</td>
                            <td>${consulta.estado}</td>
                            <td class="mt-2">
                                <a id="guardar-id-${consulta.id}" title="calificar"
                                    class="btn btn-success bi bi-check m-1"
                                    data-bs-toggle="modal"
                                    data-bs-target="#exampleModal-${consulta.id}"></a>
                            </td>
                        </tr>`
                                : ``
                            }
                      `;
                        modal += `
                      <div class="modal fade" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
                          id="exampleModal-${consulta.id}" aria-labelledby="exampleModalLabel" aria-hidden="true">
                          <div class="modal-dialog modal-lg modal-dialog-centered">
                              <div class="modal-content">
                                  <div class="modal-header">
                                      <h5 class="modal-title" id="exampleModalLabel">
                                          Calificar Usuario
                                      </h5>
                                      <button type="button" class="btn-close" data-bs-dismiss="modal"
                                          aria-label="Close"></button>
                                  </div>
                                  <div class="modal-body">
                                      <div class="form-outline mb-5">
                                          <div class="row mt-3">
                                              <div class="col-12 mb-2">
                                                  <label for="estado" class="m-2">Usuario a calificar</label>
                                                  <h3 class="mt-2 text-center">${consulta.nombre}</h3>
                                              </div>
                                          </div>
                                          <div class="row mt-3">
                                              <div class="col-12 mb-2"
                                                  style="display: flex; flex-direction: column;">
                                                  <label for="select" class="m-3">calificacion</label>
                                                  <input id="id_tipo_usuario" name="tipo_usuario" type="hidden" value="3">
                                                  <form>
                                                      <p class="clasificacion">
                                                          <input id="radio1-${consulta.id}" type="radio"
                                                              name="estrellas-${consulta.id}" value="5"><!-- --><label
                                                              for="radio1-${consulta.id}">★</label><!-- --><input
                                                              id="radio2-${consulta.id}" type="radio"
                                                              name="estrellas-${consulta.id}" value="4"><!-- --><label
                                                              for="radio2-${consulta.id}">★</label><!-- --><input
                                                              id="radio3-${consulta.id}" type="radio"
                                                              name="estrellas-${consulta.id}" value="3"><!-- --><label
                                                              for="radio3-${consulta.id}">★</label><!-- --><input
                                                              id="radio4-${consulta.id}" type="radio"
                                                              name="estrellas-${consulta.id}" value="2"><!-- --><label
                                                              for="radio4-${consulta.id}">★</label><!-- --><input
                                                              id="radio5-${consulta.id}" type="radio"
                                                              name="estrellas-${consulta.id}" value="1"><!-- --><label
                                                              for="radio5-${consulta.id}">★</label>
                                                      </p>
                                                  </form>
                                              </div>
                                          </div>
                                          <div class="row mt-3">
                                              <div class="col-12 mb-2">
                                                  <label class="form-label m-3" for="form3Example3">Observaciones</label>
                                                  <input type="text" name="observacion-${consulta.id}"
                                                      class="form-control" />
                                              </div>
                                          </div>
                                      </div>
                                  </div>
                                  <div class="modal-footer">
                                      <a  onclick="guardar_calificacion()" id="btn-guardar-calificacion" data-id="${consulta.id}"
                                          class="btn btn-success">Guardar</a>
                                      <button type="button" class="btn btn-secondary"
                                          data-bs-dismiss="modal">Cerrar</button>
                                  </div>
                              </div>
                          </div>
                      </div>
                  `;


                        $("#consultar").append(html);
                        $("#modal").append(modal);

                    });
                });

            }
            else if (calificar.tipo == "Cliente") {

                nvar.innerHTML = nvarCliente;
                h2_texto_calificar.innerHTML='Calificar Contratistas';

                let a_tipo_usuario = document.querySelector('#tipo_usuario');
                let h5_nombre_usuario = document.querySelector('#nombre_usuario');

                // Crea nodos de texto para tipo_usuario y nombre
                let tipo_usuario_texto = document.createTextNode(calificar.tipo);
                let nombre_texto = document.createTextNode(calificar.nombre);

                // Agrega los nodos de texto a los elementos del DOM
                a_tipo_usuario.appendChild(tipo_usuario_texto);
                h5_nombre_usuario.appendChild(nombre_texto);

                const objetos = JSON.parse(calificar.consulta_cliente);
                $(document).ready(function () {
                    objetos.forEach((consulta) => {
                        let html = "";
                        let modal = "";
                        html += `
                        <tr>
                        ${consulta.estado === "Finalizada"
                                ? `<tr id="fila-${consulta.id}">
                            <td scope="row">${consulta.nombre} <a style="font-size: 1.3em;"
                                    class="bi bi-person-circle m-2 "
                                    data-id="${consulta.id}"></a> </td>
                            <td>${consulta.numero}</td>
                            <td>${consulta.horario}</td>
                            <td>${consulta.direccion}</td>
                            <td>${consulta.estado}</td>
                            <td class="mt-2">
                                <a id="guardar-id-${consulta.id}" title="calificar"
                                    class="btn btn-success bi bi-check m-1"
                                    data-bs-toggle="modal"
                                    data-bs-target="#exampleModal-${consulta.id}"></a>
                            </td>
                        </tr>`
                                : ``
                            }
                      `;
                        modal += `
                      <div class="modal fade" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
                          id="exampleModal-${consulta.id}" aria-labelledby="exampleModalLabel" aria-hidden="true">
                          <div class="modal-dialog modal-lg modal-dialog-centered">
                              <div class="modal-content">
                                  <div class="modal-header">
                                      <h5 class="modal-title" id="exampleModalLabel">
                                          Calificar Usuario
                                      </h5>
                                      <button type="button" class="btn-close" data-bs-dismiss="modal"
                                          aria-label="Close"></button>
                                  </div>
                                  <div class="modal-body">
                                      <div class="form-outline mb-5">
                                          <div class="row mt-3">
                                              <div class="col-12 mb-2">
                                                  <label for="estado" class="m-2">Usuario a calificar</label>
                                                  <h3 class="mt-2 text-center">${consulta.nombre}</h3>
                                              </div>
                                          </div>
                                          <div class="row mt-3">
                                              <div class="col-12 mb-2"
                                                  style="display: flex; flex-direction: column;">
                                                  <label for="select" class="m-3">calificacion</label>
                                                  <input id="id_tipo_usuario" name="tipo_usuario" type="hidden" value="3">
                                                  <form>
                                                      <p class="clasificacion">
                                                          <input id="radio1-${consulta.id}" type="radio"
                                                              name="estrellas-${consulta.id}" value="5"><!-- --><label
                                                              for="radio1-${consulta.id}">★</label><!-- --><input
                                                              id="radio2-${consulta.id}" type="radio"
                                                              name="estrellas-${consulta.id}" value="4"><!-- --><label
                                                              for="radio2-${consulta.id}">★</label><!-- --><input
                                                              id="radio3-${consulta.id}" type="radio"
                                                              name="estrellas-${consulta.id}" value="3"><!-- --><label
                                                              for="radio3-${consulta.id}">★</label><!-- --><input
                                                              id="radio4-${consulta.id}" type="radio"
                                                              name="estrellas-${consulta.id}" value="2"><!-- --><label
                                                              for="radio4-${consulta.id}">★</label><!-- --><input
                                                              id="radio5-${consulta.id}" type="radio"
                                                              name="estrellas-${consulta.id}" value="1"><!-- --><label
                                                              for="radio5-${consulta.id}">★</label>
                                                      </p>
                                                  </form>
                                              </div>
                                          </div>
                                          <div class="row mt-3">
                                              <div class="col-12 mb-2">
                                                  <label class="form-label m-3" for="form3Example3">Observaciones</label>
                                                  <input type="text" name="observacion-${consulta.id}"
                                                      class="form-control" />
                                              </div>
                                          </div>
                                      </div>
                                  </div>
                                  <div class="modal-footer">
                                      <a  onclick="guardar_calificacion()" id="btn-guardar-calificacion" data-id="${consulta.id}"
                                          class="btn btn-success">Guardar</a>
                                      <button type="button" class="btn btn-secondary"
                                          data-bs-dismiss="modal">Cerrar</button>
                                  </div>
                              </div>
                          </div>
                      </div>
                  `;


                        $("#consultar").append(html);
                        $("#modal").append(modal);

                    });
                });
            }

        })

        .catch(function (error) {
            console.error('Error al cargar los archivos:', error);
        });

});



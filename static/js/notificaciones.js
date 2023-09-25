var token = localStorage.getItem('jwt-token');

function notificacion() {
  document.querySelector('#notificaciones').addEventListener('click', () => {
    $.ajax({
      url: 'http://localhost:3000/notificacion',
      method: 'GET',
      dataType: 'json',
      contentType: 'application/json',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      },
      success: function (notificaciones) {

        let consulta = notificaciones.informacion;

        consulta.forEach((notifi) => {
          let contenido = `
          ${!notifi.estado ?
              `
              <div id="contenedor_notificacion_${notifi.id}" class="card mb-3" style="max-width: 540px;">
              <div class = "row g-0">
                  <div class="col-md-10">
                      <div class="card-body">
                          <h5 class = "card-title">Solicitud de ${notifi.titulo}</h5>
                          <p class = "card-text">${notifi.contenido}</p>
                          <p class="card-text"><small class="text-muted">Notificaion enviada hace ${notifi.tiempo_transcurrido} </small></p>
                      </div>
                      ${!notifi.leido ?
                `
                        <span id="notificacion_leida_${notifi.id}" style="display: block;" class="position-absolute top-0 start-100 translate-middle p-2 bg-success border border-light rounded-circle">
                        </span>`
                :
                `<span id="notificacion_leida_${notifi.id}" style="display: none;" class="position-absolute top-0 start-100 translate-middle p-2 bg-success border border-light rounded-circle">
                         </span>`
              }
                  </div>
                  <div class="col-md-2 d-flex align-items-center">
                      <div class="btn-group ">
                          <a class="btn-primary  btn-circle" data-bs-toggle="dropdown" aria-expanded="false">
                              <i class="bi bi-three-dots"></i>
                          </a>
                          <ul class="dropdown-menu">
                              <li id="leido"> 
                                <a id = "${notifi.id}" class="dropdown-item marca-leida"> 
                                  <i class="bi bi-check2"></i> 
                                  ${!notifi.leido ?
                `Marcar como leída`
                :
                `Marcar como no leída`
              }
                                 
                                </a>
                              </li>

                              <li id="eliminar">
                                <a id="${notifi.id}" class="dropdown-item"><i class="bi bi-x-square"></i> 
                                  Eliminar notificación
                                </a>
                              </li>
                          </ul>
                      </div>
                  </div>
              </div>
          </div>`
              : ``}
              `;
          $("#contenido_notificaciones").append(contenido);

        });

        marcar_leido();
        eliminar();

      }
    });
    $("#contenido_notificaciones").empty();



  })
}

function marcar_leido() {
  var token = localStorage.getItem('jwt-token');
  let li = document.querySelectorAll('#leido');
  li.forEach((elemento) => {
    elemento.addEventListener('click', function (event) {

      let id_notificacion = event.target.id;
      let span = document.querySelector(`#notificacion_leida_${id_notificacion}`);

      $.ajax({
        url: 'http://localhost:3000/leer_notificacion',
        method: 'POST',
        data: JSON.stringify(id_notificacion),
        dataType: 'json',
        contentType: 'application/json',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        success: function (estado) {
          var activar = estado.leer;
          if (activar) {
            $(`#${id_notificacion}`).text("Marcar como no leída");
            span.style.display = 'none';
          } else {
            $(`#${id_notificacion}`).text("Marcar como leída");
            span.style.display = 'block';
          }
        }
      });
    });
  });
}


function eliminar() {
  var token = localStorage.getItem('jwt-token');
  let li = document.querySelectorAll('#eliminar');

  li.forEach((elementos) => {
    elementos.addEventListener('click', (event) => {

      let id_eliminar_notificacion = event.target.id;
      let contenedor_notificacion = document.querySelector(`#contenedor_notificacion_${id_eliminar_notificacion}`);

      $.ajax({
        url: 'http://localhost:3000/eliminar_notificacion',
        method: 'POST',
        data: JSON.stringify(id_eliminar_notificacion),
        dataType: 'json',
        contentType: 'application/json',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        success: function (estado) {
          var eliminado = estado.eliminar;

          if (eliminado) {
            contenedor_notificacion.remove();
          }
        }
      })

    })

  })

}
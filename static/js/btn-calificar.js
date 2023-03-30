document.querySelectorAll('#btn-guardar-calificacion').forEach(btn => {
    btn.addEventListener('click', function() {
      const id_calificacion = this.dataset.id;
      const estrellas = document.querySelector('input[name="estrellas-' + id_calificacion + '"]:checked').value;
      const observacion = document.querySelector('input[name="observacion"]').value;
  
      // Realiza la petición AJAX y maneja la respuesta del servidor
      $.ajax({
        url: '/guardar-calificacion',
        method: 'POST',
        data: JSON.stringify(
            {
                id_calificacion: id_calificacion,
                estrellas: estrellas,
                observacion: observacion
            }
        ),
        dataType: 'json',
        contentType: 'application/json',
        success: function (respuesta) {
            // Manejar la respuesta del servidor
            console.log(respuesta.recargar);
            // Cerrar la ventana modal
            window.location.href = respuesta.recargar
            $('#exampleModal-' + id_calificacion).modal('hide');
        },
        error: function (error) {
            console.log(error);
        }
    });
    });
  });
  
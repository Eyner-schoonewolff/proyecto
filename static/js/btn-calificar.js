document.querySelectorAll('#btn-guardar-calificacion').forEach(btn => {
    btn.addEventListener('click', function () {
        const id_solicitud = this.dataset.id;
        const id_tipo_usuario = document.querySelector("#id_tipo_usuario").value;
        const estrellas = document.querySelector('input[name="estrellas-' + id_solicitud + '"]:checked').value;
        const observacionInput = document.querySelector('input[name="observacion-' + id_solicitud + '"]');
        const observacion = observacionInput.value;

        // Realiza la petición AJAX y maneja la respuesta del servidor
        $.ajax({
            url: '/guardar-calificacion',
            method: 'POST',
            data: JSON.stringify(
                {
                    id_solicitud: id_solicitud,
                    id_tipo_usuario: id_tipo_usuario,
                    estrellas: estrellas,
                    observacion: observacion
                }
            ),
            dataType: 'json',
            contentType: 'application/json',
            success: function (respuesta) {
                if (respuesta.actualizar) {
                    $('#exampleModal-' + id_solicitud).modal('hide');
                    Swal.fire({
                        title: "¡Éxito!",
                        text: "Se ha realizado correctamente la calificacion",
                        icon: "success",
                        confirmButtonText: "Aceptar",
                      }).then(() => {
                        window.location.href = respuesta.recargar;
                      });
                    
                }else{
                    Swal.fire({
                        title: "Problema",
                        text: "ya se realizo la calificacion a este usuario.",
                        icon: "error",
                        confirmButtonText: "Aceptar",
                      }).then(() => {
                        window.location.href = respuesta.recargar;
                      });
                      
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});

function guardar_calificacion() {
    document.querySelectorAll('#btn-guardar-calificacion').forEach(btn => {
        btn.addEventListener('click', function () {
            let token = localStorage.getItem('jwt-token');

            const id_solicitud = this.dataset.id;
            const id_tipo_usuario = document.querySelector("#id_tipo_usuario").value;
            const estrellasInput = document.querySelector('input[name="estrellas-' + id_solicitud + '"]:checked');
            const observacionInput = document.querySelector('input[name="observacion-' + id_solicitud + '"]');
            const observacion = observacionInput ? observacionInput.value.trim() : ''; // Verifica si observacionInput existe antes de acceder a su valor

            // Verifica si los elementos existen antes de acceder a sus propiedades o métodos
            if (!id_solicitud || !id_tipo_usuario || !estrellasInput || !observacionInput) {
                Swal.fire({
                    title: "Error",
                    text: "Por favor, completa todos los campos",
                    icon: "error",
                    confirmButtonText: "Aceptar",
                });
                return; // Detiene la ejecución del código si hay campos vacíos
            }
            // Accede a la propiedad value del elemento estrellasInput
            const estrellas = estrellasInput.value;

            // Realiza la petición AJAX y maneja la respuesta del servidor
            $.ajax({
                url: 'http://localhost:3000/guardar-calificacion',
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
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
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

                    } else {
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
}


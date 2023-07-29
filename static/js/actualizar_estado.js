
function guardar_estado() {
    document.querySelectorAll("#btn-guardar-estado").forEach(function (button) {
        button.addEventListener('click', function () {
            var token = localStorage.getItem('jwt-token');
            var estado_actual = this.closest('.modal-content').querySelector("#estado_actual").innerText;
            var id_consulta = this.closest('.modal-content').querySelector("#id_consulta").value;
            var estado = this.closest('.modal-content').querySelector("#select_estado").value;

            if (estado_actual == 'Pendiente') {
                var fecha_actualizar = this.closest('.modal-content').querySelector("#fecha_actualizar").value;
                var hora_actualizar = this.closest('.modal-content').querySelector("#hora_actualizar").value;

                if (fecha_actualizar) {
                    var fecha = new Date(fecha_actualizar);
                    var anio = fecha.getFullYear();
                    var mes = ("0" + (fecha.getMonth() + 1)).slice(-2);
                    var dia = ("0" + fecha.getDate()).slice(-2);
                    var fechaFormateada = anio + "-" + mes + "-" + dia;
                }

                var fecha_actual = this.closest('.modal-content').querySelector("#fecha_actual").value;
                var hora_actual = this.closest('.modal-content').querySelector("#hora_actual").value;


                fecha_actualizar = fecha_actualizar.trim() === '' ? fecha_actual : fechaFormateada;
                hora_actualizar = hora_actualizar.trim() === '' ? hora_actual : hora_actualizar;



                $.ajax({
                    url: 'http://localhost:3000/actualizar_estado/' + id_consulta,
                    method: 'POST',
                    data: JSON.stringify(
                        {
                            estado_actual: estado_actual,
                            id: estado,
                            fecha: fecha_actualizar,
                            hora: hora_actualizar
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
                            Swal.fire({
                                title: "¡Éxito!",
                                text: "Se ha realizado correctamente la actualizacion",
                                icon: "success",
                                confirmButtonText: "Aceptar",
                            }).then(() => {
                                window.location.reload();
                            });
                        }
                    }
                });

            } else {
                $.ajax({
                    url: 'http://localhost:3000/actualizar_estado/' + id_consulta,
                    method: 'POST',
                    data: JSON.stringify(
                        {
                            estado_actual: estado_actual,
                            id: estado,
                        }
                    ),
                    dataType: 'json',
                    contentType: 'application/json',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token
                    },
                    success: function (respuesta) {
                        console.log(respuesta)
                        if (respuesta.actualizar) {
                            Swal.fire({
                                title: "¡Éxito!",
                                text: "Se ha realizado correctamente la actualizacion",
                                icon: "success",
                                confirmButtonText: "Aceptar",
                            }).then(() => {
                                window.location.reload();
                            });
                        }
                    }
                });
            }
        });
    });
}
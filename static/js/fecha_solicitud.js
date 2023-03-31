var fecha_act = new Date();
$('#fecha').datetimepicker({
    format: 'YYYY-MM-DD',
    minDate: fecha_act,

})

function guardarsolicitud() {
    let formData = new FormData();
    let fecha = $("#fecha").val();
    let hora = $("#hora").val();
    // let servicio = $("#opciones").val();
    let contratista = $("#contratistas").val();
    let problema = $("#carta").val();
    let evidencia = $("#formFileSm")[0].files[0];

    formData.append('fecha', fecha);
    formData.append('hora', hora);
    // formData.append('servicio', servicio);
    formData.append('contratista', contratista);
    formData.append('problema', problema);
    formData.append('evidencia', evidencia);

    $.ajax({
        url: '/solicitar_serv',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,

        success: function (respuesta) {
            console.log(respuesta.numero);
            if (respuesta.numero == 1) {
                Swal.fire({
                    title: "¡Éxito!",
                    text: "Se ha realizado correctamente la solicitud",
                    icon: "success",
                    confirmButtonText: "Aceptar",
                  }).then(() => {
                      $("#fecha").val('');
                      $("#hora").val('');
                      // $("#opciones").val();
                      $("#contratistas").val();
                      $("#formFileSm").val();
                      $("#carta").val('');
                  });
            } else {
                alert('Error')
            }
        }
    });
}

document.querySelector("#opciones")
    .addEventListener("change",
        (event) => {
            $.ajax({
                url: '/solicitar',
                method: 'POST',
                data: JSON.stringify(
                    { id: event.target.value }
                ),
                dataType: 'json',
                contentType: 'application/json',
                success: function (respuesta) {
                    // Actualizar opciones del select
                    var opciones = respuesta.contratista_consulta;
                    var select = document.querySelector("#contratistas");
                    select.innerHTML = "";

                    if (opciones == 0) {
                        select.innerHTML = "";
                    } else {
                        opciones[0].forEach((contratista) => {
                            select.innerHTML += '<option value="' + contratista.id + '">' + contratista.nombre + '</option>';
                        });
                    }


                }
            });
        }
    );

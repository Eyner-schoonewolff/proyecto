
var fecha_act = new Date();
$('#fecha').datetimepicker({
    format: 'YYYY-MM-DD',
    minDate: fecha_act,

})


function guardarsolicitud() {
    let fecha = $("#fecha").val();
    let hora = $("#hora").val();
    let servicio = $("#opciones").val();
    let contratista = $("#contratistas").val();
    let evidencia = $("#formFileSm").val();
    let problema = $("#carta").val();

    datos = {
        fecha,
        hora,
        servicio,
        contratista,
        evidencia,
        problema

    }

    $.ajax({
        url: '/solicitar_serv',
        method: 'POST',
        data: JSON.stringify(datos),
        contentType: "application/json; charset=utf-8",
        dataType: "json",

        success: function (respuesta) {
            console.log(respuesta.numero);
            if (respuesta.numero == 1) {
                alert('Solicitud Creada')
                $("#fecha").val('');
                $("#hora").val('');
                $("#opciones").val();
                $("#contratistas").val();
                $("#formFileSm").val();
                $("#carta").val('');
            } else {
                alert('Error')
            }
        }
    });
}
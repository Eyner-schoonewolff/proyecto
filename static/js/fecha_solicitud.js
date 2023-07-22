let token = localStorage.getItem('jwt-token');
let respuesta = { nombre: "", tipo: "" };


function guardarsolicitud() {
    const formData = new FormData();
    let fecha = $("#fecha").val();
    let hora = $("#hora").val();
    let servicio = $("#opciones").val();
    let contratista = $("#contratistas").val();
    let problema = $("#carta").val();
    let evidencia = $("#formFileSm")[0].files[0];

    if (evidencia) {
        formData.append('evidencia', evidencia);
    }

    else if (!evidencia && !$("#formFileSm").val()) {
        formData.append('evidencia', '');
    }

    formData.append('fecha', fecha);
    formData.append('hora', hora);
    formData.append('servicio', servicio);
    formData.append('contratista', contratista);
    formData.append('problema', problema);


    $.ajax({
        url: 'http://127.0.0.1:3000/solicitar_serv',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            'Authorization': 'Bearer ' + token
            // 'Content-Type': 'multipart/form-data'
        },
        success: function (respuesta) {
            console.log(respuesta.numero);
            if (respuesta.numero == 1) {
                setTimeout(function () {
                    Swal.fire({
                        title: "¡Éxito!",
                        text: "Se ha realizado correctamente la solicitud",
                        icon: "success",
                        confirmButtonText: "Aceptar",
                    }).then(() => {
                        $("#fecha").val('');
                        $("#hora").val('');
                        $("#opciones").val();
                        $("#contratistas").val();
                        $("#formFileSm").val();
                        $("#carta").val('');
                    });
                }, 1000);

            } else {
                alert('Error')
            }
        }

    });


}


Promise.all([
    $.ajax({ url: '../templates/NvarCliente.html', type: 'GET', dataType: 'html' }),
    $.ajax({
        url: 'http://localhost:3000/solicitar_serv',
        type: 'GET',
        data: JSON.stringify(respuesta),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
    })
])
    .then(function (responses) {
        let nvarCliente = responses[0];
        let data = responses[1]
        let tipo_usuario = data.tipo;

        let nvar = document.getElementById('nvar');
        nvar.innerHTML = nvarCliente;

        let a_tipo_usuario = document.querySelector('#tipo_usuario');
        let h5_nombre_usuario = document.querySelector('#nombre_usuario');

        let nombre = data.nombre;
        // Crea nodos de texto para tipo_usuario y nombre
        let tipo_usuario_texto = document.createTextNode(tipo_usuario);
        let nombre_texto = document.createTextNode(nombre);

        // Agrega los nodos de texto a los elementos del DOM
        a_tipo_usuario.appendChild(tipo_usuario_texto);
        h5_nombre_usuario.appendChild(nombre_texto);
    })
    .catch(function (error) {
        console.error('Error al cargar los archivos:', error);
    });


var fecha_act = new Date();
$('#fecha').datetimepicker({
    format: 'YYYY-MM-DD',
    minDate: fecha_act,

})


document.querySelector("#opciones")
    .addEventListener("change",
        (event) => {
            $.ajax({
                url: 'http://localhost:3000/solicitar',
                method: 'POST',
                data: JSON.stringify(
                    { id: event.target.value }
                ),
                dataType: 'json',
                contentType: 'application/json',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
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

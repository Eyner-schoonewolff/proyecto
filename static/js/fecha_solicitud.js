let token = localStorage.getItem('jwt-token');
let respuesta = { nombre: "", tipo: "" };

const fileInput = document.querySelector('#formFileSm');

// Listen for the change event so we can capture the file
const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
});

fileInput.addEventListener("change", function () {
    Main()
})

async function Main() {
    const file = document.querySelector('#formFileSm').files[0];
    fileInput.data = await toBase64(file);
}


async function guardarsolicitud() {
    let request = {
        fecha: $("#fecha").val(),
        hora: $("#hora").val(),
        servicio: $("#opciones").val(),
        nombre_servicio: $("#opciones option:selected").text(),
        contratista: $("#contratistas").val(),
        problema: $("#carta").val(),
        evidencia: fileInput.data || '',
    }

    try {
        const respuesta = await $.ajax({
            url: 'http://127.0.0.1:3000/solicitar_serv',
            method: 'POST',
            data: JSON.stringify(request),
            contentType: "application/json", // Especificar el tipo de contenido como JSON
            dataType: "json",
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });

        if (respuesta.numero == 1) {
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
                $("#formFileSm").val('');
                $("#carta").val('');
            });
        } else {
            alert('Error')
        }
    } catch (error) {
        console.error(error);
    }
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


        document.querySelector("#logout")
            .addEventListener("click",
                () => {
                    $.ajax({
                        url: 'http://localhost:3000/logout',
                        method: 'GET',
                        dataType: 'json',
                        contentType: 'application/json',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + token
                        },
                        success: function (respuesta) {
                            if (respuesta.message == 'ok') {
                                localStorage.removeItem('jwt-token');
                                window.location.href = '../templates/index.html'
                            }
                        }
                    });
                }
            );
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

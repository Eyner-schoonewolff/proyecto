document.querySelector("#btn-registro").addEventListener('click', () => {
    rol = document.querySelector("#rol").value
    email = document.querySelector("#email").value
    nombre = document.querySelector("#nombre").value
    contrasenia = document.querySelector("#contrasenia").value
    numero_documento = document.querySelector('#numeroDocumento').value
    tipo_documento = document.querySelector("#documento").value


    if (!rol || !email || !nombre || !contrasenia || !numero_documento || !tipo_documento) {
        Swal.fire({
            title: "Error",
            text: "Por favor, completa todos los campos",
            icon: "error",
            confirmButtonText: "Aceptar",
        }).then(() => {
            window.location.reload();
        });
        return; // Detiene la ejecución del código si hay campos vacíos
    }

    datos = {
        email,
        rol,
        nombre,
        contrasenia,
        tipo_documento,
        numero_documento
    }

    $.ajax({
        url: '/auth_registro',
        method: 'POST',
        data: JSON.stringify(datos),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (respuesta) {
            if (respuesta.registro) {
                Swal.fire({
                    title: "¡Éxito!",
                    text: "Se ha creado el usuario correctamente",
                    icon: "success",
                    confirmButtonText: "Aceptar",
                }).then(() => {
                    window.location.href = respuesta.home
                });
            } else {
                console.log(respuesta.mensaje)
                Swal.fire({
                    title: "Problema",
                    text: respuesta.mensaje,
                    icon: "error",
                    confirmButtonText: "Aceptar",
                }).then(() => {
                    $("#email").val('');
                    $("#nombre").val('');
                    $("#numeroDocumento").val('');
                    location.reload();
                });
            }
        }
    });

});
document.querySelector("#btn-registro").addEventListener('click', () => {
    rol = document.querySelector("#seleccion_rol").value
    email = document.querySelector("#email").value
    nombre = document.querySelector("#nombre").value
    contrasenia = document.querySelector("#contrasenia").value
    numero_documento = document.querySelector('#numeroDocumento').value
    tipo_documento = document.querySelector("#documento").value
    descripcion = document.querySelector('#descricpion_input')
    descripcion = descripcion.value ?? "" ;

    console.log(descripcion);
    if (rol == 0) {
        Swal.fire({
            title: "Problema",
            text: 'Debes elegir uno de los dos roles que aparecen',
            icon: "error",
            confirmButtonText: "Aceptar",
        }).then(() => {
            $("#email").val('');
            $("#nombre").val('');
            $("#numeroDocumento").val('');
            location.reload();
        });
        return;
    }

    if (!rol || !email || !nombre || !contrasenia || !numero_documento || !tipo_documento && rol == 3) {
        Swal.fire({
            title: "Error",
            text: "Por favor, completa todos los campos del cliente",
            icon: "error",
            confirmButtonText: "Aceptar",
        }).then(() => {
            window.location.href = '/registrar';
        });
        return; // Detiene la ejecución del código si hay campos vacíos
    }
    else if (!rol || !email || !nombre || !contrasenia || !numero_documento || !tipo_documento || !descripcion && rol == 2) {
        Swal.fire({
            title: "Error",
            text: "Por favor, completa todos los campos del contratista",
            icon: "error",
            confirmButtonText: "Aceptar",
        }).then(() => {
            window.location.href = '/registrar';
        });
        return;
    }

    datos = {
        email,
        rol,
        nombre,
        contrasenia,
        tipo_documento,
        numero_documento,
        descripcion
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


document.querySelector("#seleccion_rol")
    .addEventListener("change",
        (event) => {
            var rol = event.target.value;
            var divSelect = document.querySelector('#descricpion')

            if (rol == 2) {
                divSelect.removeAttribute('hidden', false);
            } else if (rol == 0) {
                divSelect.setAttribute('hidden', false);
            
            } else if (rol == 3) {
                divSelect.setAttribute('hidden', true);
            }
        }
    );
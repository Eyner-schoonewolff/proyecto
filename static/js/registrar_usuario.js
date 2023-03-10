document.querySelector("#btn-registro").addEventListener('click', () => {
    rol = document.querySelector("#rol").value
    email = document.querySelector("#email").value
    nombre = document.querySelector("#nombre").value
    contrasenia = document.querySelector("#contrasenia").value
    numero_documento = document.querySelector('#numeroDocumento').value
    tipo_documento = document.querySelector("#documento").value

    datos = {
        email,
        rol,
        nombre,
        contrasenia,
        tipo_documento,
        numero_documento
    }

    $.ajax({
        url: '/auth_register',
        method: 'POST',
        data: JSON.stringify(datos),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (respuesta) {
            if (respuesta.registro) {
                window.location.href = respuesta.home
            } else {
                window.location.href = respuesta.home
            }
        }
    });

});
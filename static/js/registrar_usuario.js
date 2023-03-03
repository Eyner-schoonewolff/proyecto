document.querySelector("#btn-registro").addEventListener('click', () => {
    rol = document.querySelector("#rol").value
    usuario = document.querySelector("#usuario").value
    contrasenia = document.querySelector("#contrasenia").value

    datos = {
        rol,
        usuario,
        contrasenia
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
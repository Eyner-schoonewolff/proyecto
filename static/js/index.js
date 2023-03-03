
document.querySelector("#BotonLogin").addEventListener('click', () => {
    email = document.querySelector("#inputEmail").value
    contrasenia = document.querySelector("#inputcontrasenia").value

    var datos = {
        email,
        contrasenia
    }
    $.ajax({
        url: '/auth',
        method: 'POST',
        data: JSON.stringify(datos),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (respuesta) {
            if (respuesta.login) {
                window.location.href = respuesta.home
            } else {
                window.location.href = respuesta.home;
            }
        }
    });
});

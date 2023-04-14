
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
                Swal.fire({
                    title: "¡Éxito!",
                    text: "El usuario se ha logueado correctamente",
                    icon: "success",
                    confirmButtonText: "Aceptar",
                    customClass: {
                        container: 'my-swal-container'
                      }
                  }).then(() => {
                     window.location.href = respuesta.home;
                  });
            } else {
                Swal.fire({
                    title: "Hubo un error",
                    text: respuesta.excepcion,
                    icon: "error",
                    confirmButtonText: "Aceptar",
                    customClass: {
                        container: 'my-swal-container'
                      }
                  }).then(() => {
                    window.location.href = respuesta.home;
                  });
            }
        }
    });
});

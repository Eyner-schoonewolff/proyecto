document.querySelector("#email_cambio")
    .addEventListener("input",
        (event) => {
            var nombre = document.querySelector("#nombre_completo");
            var documento = document.querySelector("#documento_numero");
            var direccion = document.querySelector("#direccion");
            var celular = document.querySelector("#cel");
            var email_actualizacion = document.querySelector("#email_actualizacion");
            const btn = document.querySelector('#btn-actuzalizar_2') 

            $.ajax({
                url: '/actualizar_admin',
                method: 'POST',
                data: JSON.stringify(
                    { email: event.target.value }
                ),
                dataType: 'json',
                contentType: 'application/json',
                success: function (respuesta) {
                    var datosPersonales = respuesta.datos;

                    if (datosPersonales == null) {
                        btn.disabled = true
                        email_actualizacion.readOnly=true;
                        email_actualizacion.value="Nah"
                        nombre.value = "Nah";
                        documento.value = 0;
                        direccion.value = "Nah";
                        celular.value = 0;

                    } else {
                        btn.disabled = false
                        email_actualizacion.readOnly=false;
                        email_actualizacion.value=""
                        nombre.value = datosPersonales.nombre;
                        documento.value = datosPersonales.documento;
                        direccion.value = datosPersonales.direccion;
                        celular.value = datosPersonales.celular;
                    }


                }
            });
        }
    );

document.querySelector("#btn-actuzalizar_2")
    .addEventListener("click",
        () => {
            email_actual = document.querySelector("#email_cambio").value;
            email_nuevo = document.querySelector("#email_actualizacion").value;

            // Validar si los valores son null o undefined
            if (email_actual === null || email_actual === undefined || email_nuevo === null || email_nuevo === undefined) {
                // Realizar acciones para manejar los valores null o undefined, como mostrar un mensaje de error, realizar acciones alternativas, etc.
                Swal.fire({
                    title: "Error",
                    text: "Por favor, completa todos los campos",
                    icon: "error",
                    confirmButtonText: "Aceptar",
                });
                return;
            }

            // Utilizar trim() en los valores obtenidos
            email_actual = email_actual.trim();
            email_nuevo = email_nuevo.trim();

            $.ajax({
                url: '/actualizar_email_usuario',
                method: 'POST',
                data: JSON.stringify(
                    {
                        email_actual: email_actual,
                        email_nuevo: email_nuevo
                    }
                ),
                dataType: 'json',
                contentType: 'application/json',
                success: function (respuesta) {
                    if(respuesta.actualizacion){
                        Swal.fire({
                            title: "¡Éxito!",
                            text: respuesta.mensaje,
                            icon: "success",
                            confirmButtonText: "Aceptar",
                        }).then(() => {
                            window.location.href = respuesta.home
                        });
                    }else{
                        Swal.fire({
                            title: "Ups.. Hay un Problema",
                            text: respuesta.mensaje_excepcion,
                            icon: "error",
                            confirmButtonText: "Aceptar",
                        }).then(() => {
                            window.location.href = respuesta.home
                        });;
                    }
                }
            });
        }
    );


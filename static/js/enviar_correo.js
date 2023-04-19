
document.querySelector("#btn-enviar-correo").
    addEventListener('click', () => {
         correo = document.querySelector('#emailContacto').value || null;
         nombre = document.querySelector('#nombreContacto').value || null;
         numero = document.querySelector('#telefonoContacto').value || null;
         asunto = document.querySelector('#asuntoContacto').value || null;
         mensaje = document.querySelector('#smsContacto').value || null;

        if (correo === null || correo === "" || nombre === null || nombre === ""
            || numero === null || numero === "" || asunto === null || asunto === ""
            || mensaje === null || mensaje === "") {
            Swal.fire({
                title: "Hubo un problema",
                text: "Por favor, verifique que todos los campos estén llenos",
                icon: "error",
                confirmButtonText: "Aceptar",
            }).then(() => {
                window.location.reload();
            });
            return;
        }

        $.ajax({
            url:'/enviar_correos',
            method: 'POST',
            data: JSON.stringify({
                correo: correo,
                nombre:nombre,
                numero:numero,
                asunto:asunto,
                mensaje:mensaje
            }),
            dataType: 'json',
            contentType: 'application/json',
            success: (respuesta) =>{
                if(respuesta.actualizar){
                    Swal.fire({
                        title: "Se ha enviado el correo exitosamente",
                        text: "Por favor espere la respuesta de serviciossbarranquilla@gmail.com",
                        icon: "success",
                        confirmButtonText: "Aceptar",
                    }).then(() => {
                      window.location.href=respuesta.endpoint;
                    });
                }else{
                    Swal.fire({
                        title: "Error",
                        text: "El correo no es un correo electronico valido",
                        icon: "error",
                        confirmButtonText: "Aceptar",
                    }).then(() => {
                        window.location.reload();
                    });
                }
            }

        });

    });
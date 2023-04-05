document.querySelectorAll(".btn-perfil").forEach(function (button) {
    button.addEventListener('click', function (event) {
        var id_perfil = event.target.parentElement.querySelector(".id_perfil").value;
        $.ajax({
            url: '/perfiles/' + id_perfil,
            method: 'POST',
            data: JSON.stringify({
                id_usuario_cliente: id_perfil
            }),
            dataType: 'json',
            contentType: 'application/json',
            success: function (respuesta) {
                if (respuesta.actualizar) {
                    
                    respuesta.datos.forEach(function (dato) {
                        var h6Nombre = document.createElement('h6');
                        h6Nombre.id = 'nombre-' + id_perfil;
                        h6Nombre.textContent = dato.nombre;

                        var h5Calificacion = document.createElement('h5');
                        h5Calificacion.id = 'calificacion-' + id_perfil;
                        h5Calificacion.textContent = dato.calificacion;
                        
                        var pComentario = document.createElement('p');
                        pComentario.id = 'comentario-' + id_perfil;
                        pComentario.textContent = dato.comentario;
                        
                        var modalBody = document.querySelector('#exampleModal-' + id_perfil + ' .modal-body');
                        modalBody.appendChild(h6Nombre);
                        modalBody.appendChild(h5Calificacion);
                        modalBody.appendChild(pComentario);
                    });
                    
                    $('#exampleModal-' + id_perfil).modal('show');
                }
            }
        });
    });
});

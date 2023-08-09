function addClickEventToButtons() {
    document.querySelectorAll(".btn-perfil").forEach(function (button) {
        button.addEventListener('click', function (event) {
            var token = localStorage.getItem('jwt-token');
            var id_perfil = event.target.parentElement.querySelector(".id_perfil").value;
            var tipo_usuario = event.target.parentElement.querySelector(".tipo_usuario_perfil") ?? null;

            if (tipo_usuario != null) {
                tipo_usuario = tipo_usuario.value
            }
            $.ajax({
                url: 'http://127.0.0.1:3000/perfiles/' + id_perfil,
                method: 'POST',
                data: JSON.stringify({
                    id_usuario_cliente: id_perfil,
                    tipo_usuario: tipo_usuario
                }),
                dataType: 'json',
                contentType: 'application/json',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
                success: function (respuesta) {
                    if (respuesta.actualizar) {
                        var div = document.querySelector(".contenedor_calificacion");
                        var modal_contenido = document.getElementById('modal_contenido');
                        var promedio = document.getElementById("promedio-calificacion");
                        modal_contenido.innerHTML = "";
                        promedio.innerHTML = "";
                        for (const calificacion of respuesta.datos) {
                            a = div.cloneNode(true);
                            a.classList.remove("d-none")

                            promedio.innerHTML = "Calificacion " + respuesta.calificacion.promedio + '★';

                            const estrellas = a.querySelectorAll('.clasificacion input[type="radio"]');
                            const valor = calificacion.valor; // Este valor podría venir de una base de datos o de un formulario

                            for (let i = 0; i < estrellas.length; i++) {
                                if (estrellas[i].value <= valor) {
                                    estrellas[i].nextElementSibling.classList.add('checked');
                                } else {
                                    estrellas[i].nextElementSibling.classList.remove('checked');
                                }
                            }

                            a.querySelector(".card-title").textContent = calificacion.nombre
                            a.querySelector(".card-text").textContent = calificacion.comentario
                            a.querySelector(".text-muted").textContent = calificacion.registro

                            modal_contenido.appendChild(a)
                        }
                        $('#exampleModal').modal('show');
                    }
                }
            });
        });
    });
}
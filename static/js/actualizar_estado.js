

document.querySelectorAll("#btn-guardar-estado").forEach(function (button) {
    button.addEventListener('click', function () {
        var id_consulta = this.closest('.modal-content').querySelector("#id_consulta").value;
        var estado = this.closest('.modal-content').querySelector("#select_estado").value;

        console.log(estado);

        $.ajax({
            url: '/actualizar_estado/' + id_consulta,
            method: 'POST',
            data: JSON.stringify(
                { id: estado }
            ),
            dataType: 'json',
            contentType: 'application/json',
            success: function (respuesta) {
                if (respuesta.actualizar) {
                    // console.log(respuesta.data)
                    window.location.href = respuesta.recargar

                }
            }
        });
    });
});



document.querySelector("#btn-actuzalizar").addEventListener('click', () => {
    nombre = document.querySelector("#nombre").value;
    direccion = document.querySelector("#direccion").value;
    numeroCelular = document.querySelector("#numeroCelular").value;
    // const agregarOcupacionElement = document.querySelector("#agregar_ocupacion");

    //si el valor de agregaOcupacion no esta definido y es null la variable devolvera el valor de 0
    // const agregar_ocupacion = agregarOcupacionElement !== null ? agregarOcupacionElement.value : 0;
    
    var datos = {
        nombre,
        direccion,
        numeroCelular,
    };

    $.ajax({
        url: '/auth_actualizar',
        method: 'POST',
        data: JSON.stringify(datos),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (respuesta) {
            if (respuesta.actualizar) {
                window.location.href = respuesta.home
            } 
        }
    });
});

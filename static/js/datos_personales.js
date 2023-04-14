
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


function ocupaciones() {
    $.ajax({
        url: '/ocupaciones_contratista',
        method: 'GET',
        processData: false,
        contentType: false,
        success: function (datos) {

            if (datos.numero == 1) {
                console.log(datos.datos);
                $.each(datos.datos, function (i, e) {
                    $("#agregar_ocupacion option[value='" + e.id + "']").prop("selected", true);
                    $("#agregar_ocupacion").select2()
                });
            } else {
                $("#agregar_ocupacion").select2()
            }
        }
    });
}


function actualizar_ocu() {
    let datos = $("#agregar_ocupacion").val()

    if (datos.length == 0) {
        Swal.fire({
            title: "",
            text: "Debe agregar una o mas ocupaciones",
            icon: "warning",
            confirmButtonText: "Aceptar",
        })
    } else {
        var datos_ = {
            datos
        };
        $.ajax({
            url: '/agregar_ocupaciones',
            method: 'POST',
            data: JSON.stringify(datos_),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (respuesta) {
                if (respuesta.numero == 1){
                    Swal.fire({
                        title: "",
                        text:   "Se agregaron las ocupaciones correctamente",
                        icon: "success",
                        showConfirmButton: false,
                        timer:1500 
                    })
                    setTimeout(() => {
                        window.location.reload()
                    }, 1600);
                }else{
                    Swal.fire({
                        title: "",
                        text:   "Se actualizaron las ocupaciones correctamente",
                        icon: "info",
                        showConfirmButton: false,
                        timer:1500
                    })
                    setTimeout(() => {
                        window.location.reload()
                        
                    }, 1600);
                }
            }
        });
    }

}

ocupaciones()


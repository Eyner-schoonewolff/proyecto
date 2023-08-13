let tokenExpirationTime = localStorage.getItem('exp');
console.log(tokenExpirationTime);
var timeString = localStorage.getItem('exp_seg');;
let timeout;

currentTime = Math.floor(Date.now() / 1000); // Tiempo actual en formato UNIX (segundos)

let inactivityTimeout = tokenExpirationTime - currentTime; // Calcula el tiempo restante del token en segundos

function timeToSeconds(timeString) {
    let [hours, minutes, seconds] = timeString.split(':').map(Number);
    return hours * 3600 + minutes * 60 + seconds;
}


let segundos = timeToSeconds(timeString);

function resetTimer() {
    clearTimeout(timeout);
    timeout = setTimeout(checkTokenExpiration, segundos * 1000);
}

$(document).on("mousemove keydown", function () {
    resetTimer();
});

$(document).ready(function () {
    resetTimer();
});


// function protectedRequest() {
//     const token = localStorage.getItem('jwt-token');
//     if(token){
//         $.ajax({
//             url: 'http://localhost:3000/proteccion',
//             type: 'GET',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Authorization': 'Bearer ' + token
//             },
//             success: function (data) {
//                 console.log(data.mensaje);
//             },
//             error: function (xhr, status, error) {
//                 if (xhr.status === 401) {
//                     console.log('Token expirado. Redirigiendo...');
//                     alert('Sesión expirada');
//                     // Realiza el cierre de sesión y redirige
//                     localStorage.removeItem('jwt-token');
//                     window.location.href = '../templates/index.html';
//                 } else {
//                     alert('Sesión expirada');
//                     // Realiza el cierre de sesión y redirige
//                     window.location.href = '../templates/index.html';
//                     console.log(status);
//                 }
//             }
//         });

//     }else{
//         $.ajax({
//             url: 'http://localhost:3000/proteccion',
//             type: 'GET',
//             success: function (data) {
//                 console.log(data.mensaje);
//             },
//             error: function (xhr, status, error) {
//                     alert('Sesión expirada');
//                     // Realiza el cierre de sesión y redirige
//                     window.location.href = '../templates/index.html';
//                     console.log(xhr.status);
//             }
//         });
//     }


// }


function makeAuthenticatedRequest(url, method, data) {
    var token = localStorage.getItem('jwt-token');
    return $.ajax({
        url: url,
        method: method,
        data: data,
        headers: {
            'Authorization': `Bearer ${token}` // Incluir el token en la cabecera
        }
    });
}

// Ejemplo de cómo hacer una solicitud protegida
const apiUrl = 'http://localhost:3000/proteccion';
makeAuthenticatedRequest(apiUrl, 'GET')
    .done(function (response) {
        console.log('Respuesta exitosa:', response);
    })
    .fail(function (jqXHR, textStatus) {
        console.log(jqXHR.status)
        if (jqXHR.status === 0) {
            Swal.fire({
                title: "Permiso denegado",
                text: "Debe iniciar sesión",
                type: "warning",
                confirmButtonText: "Aceptar",
                showLoaderOnConfirm: true,
            }).then(() => {
                window.location.href = '../templates/index.html';
            });
        }
    });



function checkTokenExpiration() {
    if (token) {
        const tiempo = localStorage.getItem('exp');
        // const tokenData = JSON.parse(atob(token.split('.')[1])); // Decodifica el token

        var date = new Date(tiempo);

        // Obtiene el tiempo en milisegundos
        var timeInMillis = date.getTime();

        // Convierte el tiempo en segundos dividiendo por 1000
        var unixTimestamp = Math.floor(timeInMillis / 1000);
        const expirationTime = unixTimestamp * 1000; // Convierte la expiración UNIX a milisegundos


        const tiempo_actual = Date.now();

        if (tiempo_actual >= expirationTime) {
            console.log('Token ha expirado. Cerrando sesión...');
            // Realiza el cierre de sesión y redirige
            localStorage.removeItem('jwt-token');
            Swal.fire({
                title: "La Sesion ha caducado",
                text: "Vuela a iniciar sesión",
                type: "warning",
                confirmButtonText: "Aceptar",
                showLoaderOnConfirm: true,
            }).then(() => {
                window.location.href = '../templates/index.html';
            });
        }
    }
}

// Ejecuta la función de verificación cada cierto intervalo de tiempo
// setInterval(checkTokenExpiration, 10000); // Verificar cada 10 segundos (ajusta según tus necesidades)

// // Ejecuta la función para realizar la solicitud protegida
// protectedRequest();

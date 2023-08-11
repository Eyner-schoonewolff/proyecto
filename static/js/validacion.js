// Función para realizar solicitudes protegidas utilizando AJAX

var tokenExpirationTime = localStorage.getItem('exp');
// var currentTime = Math.floor(Date.now() / 1000); // Tiempo actual en formato UNIX (segundos)
var timeString = localStorage.getItem('exp_seg');;
// var inactivityTimeout = tokenExpirationTime - currentTime; // Calcula el tiempo restante del token en segundos
console.log(timeString)
var timeout;

var currentTime = Math.floor(Date.now() / 1000); // Tiempo actual en formato UNIX (segundos)

var inactivityTimeout = tokenExpirationTime - currentTime; // Calcula el tiempo restante del token en segundos

function timeToSeconds(timeString) {
    const [hours, minutes, seconds] = timeString.split(':').map(Number);
    return hours * 3600 + minutes * 60 + seconds;
}


const seconds = timeToSeconds(timeString);
// console.log(seconds);

function resetTimer() {
    clearTimeout(timeout);
    timeout = setTimeout(checkTokenExpiration, seconds * 1000);
    // timeout = setTimeout(checkTokenExpiration, 60 * 1000);
}

$(document).on("mousemove keydown", function () {
    resetTimer();
});

$(document).ready(function () {
    resetTimer();
});


// function protectedRequest() {
//     const token = localStorage.getItem('jwt-token');
//     $.ajax({
//         url: 'http://localhost:3000/proteccion',
//         type: 'GET',
//         headers: {
//             'Content-Type': 'application/json',
//             'Authorization': 'Bearer ' + token
//         },
//         success: function (data) {
//             console.log(data.mensaje);
//         },
//         error: function (xhr, status, error) {
//             if (xhr.status === 401) {
//                 console.log('Token expirado. Redirigiendo...');
//                 alert('Sesión expirada');
//                 // Realiza el cierre de sesión y redirige
//                 localStorage.removeItem('jwt-token');
//                 window.location.href = '../templates/index.html';
//             } else {
//                 console.log('Error:', xhr.responseText);
//                 console.log('--------------');
//             }
//         }
//     });
// }
var token = localStorage.getItem('jwt-token');

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


        const currentTime = Date.now();

        if (currentTime >= expirationTime) {
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

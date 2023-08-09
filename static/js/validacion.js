// Función para realizar solicitudes protegidas utilizando AJAX
function protectedRequest() {
    const token = localStorage.getItem('jwt-token');
    $.ajax({
        url: 'http://localhost:3000/proteccion',
        type: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        success: function (data) {
            console.log(data.mensaje);
        },
        error: function (xhr, status, error) {
            if (xhr.status === 401) {
                console.log('Token expirado. Redirigiendo...');
                alert('Sesión expirada');
                // Realiza el cierre de sesión y redirige
                localStorage.removeItem('jwt-token');
                window.location.href = '../templates/index.html';
            } else {
                console.log('Error:', xhr.responseText);
                console.log('--------------');
            }
        }
    });
}

// Función para verificar si el token ha expirado
function checkTokenExpiration() {
    const token = localStorage.getItem('jwt-token');
    if (token) {
        const tokenData = JSON.parse(atob(token.split('.')[1])); // Decodifica el token
        const expirationTime = tokenData.exp * 1000; // Convierte la expiración UNIX a milisegundos
        const currentTime = Date.now();

        if (currentTime >= expirationTime) {
            console.log('Token ha expirado. Cerrando sesión...');
            // Realiza el cierre de sesión y redirige
            localStorage.removeItem('jwt-token');
            alert('Sesión expirada');
            window.location.href = '../templates/index.html';
        }
    }
}

// Ejecuta la función de verificación cada cierto intervalo de tiempo
setInterval(checkTokenExpiration, 10000); // Verificar cada 10 segundos (ajusta según tus necesidades)

// Ejecuta la función para realizar la solicitud protegida
protectedRequest();

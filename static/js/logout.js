var token = localStorage.getItem('jwt-token');
var id = localStorage.getItem('id');

function logout() {
  document.querySelector("#logout")
    .addEventListener("click",
      () => {
        $.ajax({
          url: 'http://localhost:3000/logout',
          method: 'GET',
          dataType: 'json',
          contentType: 'application/json',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          success: function (respuesta) {
            if (respuesta.message == 'ok') {
              cerrar_sala(id);
              localStorage.removeItem('jwt-token');
              localStorage.removeItem('id');
              localStorage.removeItem('exp');
              localStorage.removeItem('exp_seg');
              window.location.href = '../templates/index.html'
            }
          }
        });
      }
    );
}
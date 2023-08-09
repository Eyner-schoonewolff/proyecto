var token = localStorage.getItem('jwt-token');

function logout(){
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
              if(respuesta.message=='ok'){
                localStorage.removeItem('jwt-token');
                window.location.href='../templates/index.html'
              }
          }
      });
    }
  );
}
$(document).ready(function () {
    var respuesta = { nombre: "", tipo_usuario: "" };
    var token = localStorage.getItem('jwt-token');
  
    var request = $.ajax({
      url: 'http://localhost:3000/home',
      type: 'GET',
      data: JSON.stringify(respuesta),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      }
    });
  
    request.done(function (data) {
      // Procesa la respuesta del backend
      let nombre = data.nombre;
      let tipo_usuario = data.tipo;
  
      let a_tipo_usuario = document.querySelector('#tipo_usuario');
      let h5_nombre_usuario = document.querySelector('#nombre_usuario');
  
      // Crea nodos de texto para tipo_usuario y nombre
      let tipo_usuario_texto = document.createTextNode(tipo_usuario);
      let nombre_texto = document.createTextNode(nombre);
  
      // Agrega los nodos de texto a los elementos del DOM
      a_tipo_usuario.appendChild(tipo_usuario_texto);
      h5_nombre_usuario.appendChild(nombre_texto);
  
      console.log(data);
    });
  
    request.fail(function (jqXHR, textStatus) {
      console.log('Error en la solicitud:', textStatus);
    });
  });
  
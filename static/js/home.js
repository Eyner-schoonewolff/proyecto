$(document).ready(function () {
  var respuesta = { nombre: "", tipo_usuario: "" };
  var token = localStorage.getItem('jwt-token');
  var id = localStorage.getItem('id');

  Promise.all([
    $.ajax({ url: '../templates/NvarContratista.html', type: 'GET', dataType: 'html' }),
    $.ajax({ url: '../templates/NvarCliente.html', type: 'GET', dataType: 'html' }),
    $.ajax({
      url: 'http://localhost:3000/home',
      type: 'GET',
      data: JSON.stringify(respuesta),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      }
    })
  ])
    .then(function (responses) {
      let nvarContratista = responses[0];
      let nvarCliente = responses[1];
      let data = responses[2]
      let tipo_usuario = data.tipo;

      if (tipo_usuario === 'Contratista') {
        let nvar = document.getElementById('nvar');
        nvar.innerHTML = nvarContratista;

        let a_tipo_usuario = document.querySelector('#tipo_usuario');
        let h5_nombre_usuario = document.querySelector('#nombre_usuario');

        let nombre = data.nombre;
        // Crea nodos de texto para tipo_usuario y nombre
        let tipo_usuario_texto = document.createTextNode(tipo_usuario);
        let nombre_texto = document.createTextNode(nombre);

        // Agrega los nodos de texto a los elementos del DOM
        a_tipo_usuario.appendChild(tipo_usuario_texto);
        h5_nombre_usuario.appendChild(nombre_texto);

        // enviar_notificacion(a_tipo_usuario);
        socket.emit("join", { username: data.nombre, room: id });
      

        notificacion();
        mostrar_notificacion();
        logout();

      } else if (tipo_usuario === 'Cliente') {
        let nvar = document.getElementById('nvar');
        nvar.innerHTML = nvarCliente;
        let a_tipo_usuario = document.querySelector('#tipo_usuario');
        let h5_nombre_usuario = document.querySelector('#nombre_usuario');

        let nombre = data.nombre;
        // Crea nodos de texto para tipo_usuario y nombre
        let tipo_usuario_texto = document.createTextNode(tipo_usuario);
        let nombre_texto = document.createTextNode(nombre);

        // Agrega los nodos de texto a los elementos del DOM
        a_tipo_usuario.appendChild(tipo_usuario_texto);
        h5_nombre_usuario.appendChild(nombre_texto);

        socket.emit("join", { username: data.nombre, room: id });

        logout();
      }
    })
    .catch(function (error) {
      // window.location.href='../templates/index.html'
      console.error('Error al cargar los archivos:', error);
    });

});
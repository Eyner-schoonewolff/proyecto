// Obtener el parámetro 'imagenURL' de la URL
var token = localStorage.getItem('jwt-token');

const urlParams = new URLSearchParams(window.location.search);

const imagenURL = urlParams.get('imagenURL');
const descripcion = urlParams.get('descripcion');

var img = document.getElementById('imagen-evidencia');
img.src = imagenURL;
let descripcion_texto = document.querySelector('#evidencia-descripcion');
descripcion_texto.innerHTML = 'Descripcion: ' + descripcion;

notificacion();
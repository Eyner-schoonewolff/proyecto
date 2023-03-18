// Obtener el elemento de fecha
var fecha = document.getElementById("fecha");

// Obtener la fecha actual
var hoy = new Date().toISOString().split("T")[0];

// Establecer el valor mínimo como la fecha actual
fecha.setAttribute("min", hoy);
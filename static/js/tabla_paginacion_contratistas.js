$(document).ready(function () {
    var table = $('#paginacion_contratista').DataTable({
        language: {
            processing: "Tratamiento en curso...",
            search: "Buscar&nbsp;:",
            lengthMenu: "Agrupar de _MENU_ items",
            info: "Mostrando del item _START_ al _END_ de un total de _TOTAL_ items",
            infoEmpty: "No existen datos.",
            infoFiltered: "(filtrado de _MAX_ elementos en total)",
            infoPostFix: "",
            loadingRecords: "Cargando...",
            zeroRecords: "No se encontraron datos con tu busqueda",
            emptyTable: "No hay datos disponibles en la tabla.",
            paginate: {
                first: "Primero",
                previous: "Anterior",
                next: "Siguiente",
                last: "Ultimo"
            },
            aria: {
                sortAscending: ": active para ordenar la columna en orden ascendente",
                sortDescending: ": active para ordenar la columna en orden descendente"
            }
        },
        scrollY: 400,
        lengthMenu: [[5, 10, -1], [5, 10, "All"]],
    });

    $.fn.dataTable.ext.search.push(
        function(settings, data, dataIndex) {
            var min = $('#min').val();
            var max = $('#max').val();
            var date = new Date(data[2]); // asumiendo que la columna de fecha es la primera (índice 0)
            if ((min === '' && max === '') ||
                (min === '' && date <= new Date(max)) ||
                (max === '' && date >= new Date(min)) ||
                (date >= new Date(min) && date <= new Date(max))) {
                return true;
            }

            return false;
        }
    );

    // Configurar los campos de entrada de fecha
    $('<input type="date" id="min" />').appendTo('#paginacion_contratista_filter');
    $('<input type="date" id="max" />').appendTo('#paginacion_contratista_filter');

    // Agregar el evento de cambio en los campos de entrada de fecha
    $('#min, #max').on('change', function() {
        table.draw();
    });

    // Redibujar la tabla al cambiar los campos de entrada de fecha
    table.draw();
});

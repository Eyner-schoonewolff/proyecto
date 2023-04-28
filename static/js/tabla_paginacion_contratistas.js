$(document).ready(function () {
    var table = $('#paginacion_usuarios').DataTable({
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
            responsive: "true",
            aria: {
                sortAscending: ": active para ordenar la columna en orden ascendente",
                sortDescending: ": active para ordenar la columna en orden descendente"
            }
        },
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: '<i class="fas fa-file-excel"></i> ',
                titleAttr: 'Exportar a Excel',
                className: 'btn btn-success'
            },
            {
                extend: 'pdfHtml5',
                text: '<i class="fas fa-file-pdf"></i> ',
                titleAttr: 'Exportar a PDF',
                className: 'btn btn-danger'
            },
            {
                extend: 'print',
                text: '<i class="fa fa-print"></i> ',
                titleAttr: 'Imprimir',
                className: 'btn btn-info'
            },
        ],
        scrollY: 400,
        lengthMenu: [[5, 10, -1], [5, 10, "All"]],
    });
    $.fn.dataTable.ext.search.push(
        function (settings, data, dataIndex) {
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

    $(document).ready(function() {
        var table = $('#myTable').DataTable();
      
        $('.dt-button buttons-print btn btn-info').on('click', function() {
          var printColumns = [0, 1, 2]; // índices de las columnas a imprimir
          var columnCount = table.columns()[0].length;
      
          for (var i = 0; i < columnCount; i++) {
            var column = table.column(i);
      
            if (printColumns.indexOf(i) !== -1) {
              // mostrar columnas a imprimir
              column.visible(true);
            } else {
              // ocultar columnas que no se van a imprimir
              column.visible(false);
            }
          }
      
          // abrir ventana de impresión
          window.print();
      
          // restaurar visibilidad de todas las columnas
          table.columns().visible(true);
        });
      });
      
      

    $(document).ready(function () {
        var pickerMin = new Pikaday({
            field: document.getElementById('min'),
            format: 'D MMM YYYY',
            i18n: {
                previousMonth: 'Mes anterior',
                nextMonth: 'Mes siguiente',
                months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
                weekdays: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
                weekdaysShort: ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
            },
            onSelect: function () {
                table.draw();
            },
            onClose: function () {
                if ($('#min').val() == null || $('#min').val() == '') {
                  $('#min').val('');
                  table.draw();
                }
              },
        });
        var pickerMax = new Pikaday({
            field: document.getElementById('max'),
            format: 'YYYY-MM-DD',
            i18n: {
                previousMonth: 'Mes anterior',
                nextMonth: 'Mes siguiente',
                months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
                weekdays: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
                weekdaysShort: ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
            },
            onSelect: function () {
                table.draw();
            },
            onClose: function () {
                if ($('#max').val() == null || $('#max').val() == '') {
                  $('#max').val('');
                  table.draw();
                }
              },
        });

    });

    // Redibujar la tabla al cambiar los campos de entrada de fecha
});

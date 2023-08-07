// function paginacion() {

//     $(document).ready(function () {
//         $('#paginacion').DataTable({
//             language: {
//                 processing: "Tratamiento en curso...",
//                 search: "Buscar&nbsp;:",
//                 lengthMenu: "Agrupar de _MENU_ items",
//                 info: "Mostrando del item _START_ al _END_ de un total de _TOTAL_ items",
//                 infoEmpty: "No existen datos.",
//                 infoFiltered: "(filtrado de _MAX_ elementos en total)",
//                 infoPostFix: "",
//                 loadingRecords: "Cargando...",
//                 zeroRecords: "No se encontraron datos con tu busqueda",
//                 emptyTable: "No hay datos disponibles en la tabla.",
//                 paginate: {
//                     first: "Primero",
//                     previous: "Anterior",
//                     next: "Siguiente",
//                     last: "Ultimo"
//                 },
//                 aria: {
//                     sortAscending: ": active para ordenar la columna en orden ascendente",
//                     sortDescending: ": active para ordenar la columna en orden descendente"
//                 }
//             },
//             dom: 'Bfrtip',
//             buttons: [
//                 {
//                     extend: 'excelHtml5',
//                     text: '<i class="fas fa-file-excel"></i> ',
//                     titleAttr: 'Exportar a Excel',
//                     className: 'btn btn-success'
//                 },
//                 {
//                     extend: 'pdfHtml5',
//                     text: '<i class="fas fa-file-pdf"></i> ',
//                     titleAttr: 'Exportar a PDF',
//                     className: 'btn btn-danger'
//                 },
//                 {
//                     extend: 'print',
//                     text: '<i class="fa fa-print"></i> ',
//                     titleAttr: 'Imprimir',
//                     className: 'btn btn-info'
//                 },
//             ],
//             scrollY: 400,
//             lengthMenu: [[5, 10, -1], [5, 10, "All"]],
//         });
//     });
// }
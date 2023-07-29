
var token = localStorage.getItem('jwt-token');
function llenardatos(params) {

    $.ajax({
        url: 'http://localhost:3000/datosestadisticas',
        method: 'GET',
        async: false,
        contentType: "application/json; charset=utf-8",
            dataType: "json",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
        success: function (datos) {
         
            const ctx = document.getElementById('mychart');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: datos.map(row => row.nombre),
                    datasets: [{
                        label: 'Trabajos',
                        data: datos.map(row => row.contador),
                        backgroundColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 159, 64, 1)',
                            'rgba(255, 205, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                        ],
                        borderColor: 'rgba(0, 0, 0, 1)', // Color del borde
                        borderWidth: 1
                    },

                    ],


                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },

                }
            });
        }

    })
}

function llenardatos1(params) {

    $.ajax({
        url: 'http://localhost:3000/datosestadisticaslinea',
        method: 'GET',
        async: false,
        contentType: "application/json; charset=utf-8",
            dataType: "json",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
        success: function (datos) {
     
            const ctx = document.getElementById('mychart1');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: datos.map(row => row.mes),
                    datasets: [{
                        label: 'Solicitud por mes',
                        data: datos.map(row => row.contador),
                        fill: false,
                        backgroundColor: datos.map(row => row.color),
                        borderColor: 'rgba(0,0,0)', // Color del borde
                        tension: 0.2
                    },

                    ],


                },
                options: {
                    animations: {
                        tension: {
                            duration: 1000,
                            easing: 'linear',
                            from: 1,
                            to: 0,
                            loop: true
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

    })
}

function llenardatos2(params) {

    $.ajax({
        url: 'http://localhost:3000/datosestadisticastorta',
        method: 'GET',
        async: false,
        contentType: "application/json; charset=utf-8",
            dataType: "json",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
        success: function (datos) {
        
            const ctx1 = document.getElementById('mychart2');

            new Chart(ctx1, {
                type: 'doughnut',
                data: {
                    labels: datos.map(row => row.mes),
                    datasets: [{
                        label: 'Solicitud por mes',
                        data: datos.map(row => row.prom),
                        backgroundColor: datos.map(row => row.color),
                        hoverBorderColor: 'white',
                        hoverOffset: 2,
                        borderColor: 'rgba(0, 0, 0, 1)', // Color del borde
                        borderWidth: 1
                    },

                    ],
                },
                options: {
                    rotation: -Math.PI,
                    animation: {
                        animateScale: true,
                        animateRotate: true,

                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Promedio de calificación',
                            padding: {
                                top: 10,
                                bottom: 2
                            }
                        }
                    }
                }
            });
        }

    })
}


llenardatos();
llenardatos1();
llenardatos2();
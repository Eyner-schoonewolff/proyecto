    #   SELECT s.id, (s.horario) as horario,MAX(s.hora) as hora, (e.nombre) as estado, (s.id_ocupacion_solicitud) as id_ocupacion, (o.nombre) as ocupacion,  (udp.nombre_completo) as nombre,  (udp.numero_celular) as numero,(c.id_numero_estrellas) as estrellas
    #             FROM solicitud s
    #             INNER JOIN usuarios u ON s.id_usuario_contratista=u.id
    #             INNER JOIN ocupacion o ON s.id_ocupacion_solicitud=o.id
    #             INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
    #             INNER JOIN estado e ON s.id_estado=e.id
    #             LEFT JOIN calificacion c ON c.id_solicitud=s.id
    #             WHERE s.id_usuario_cliente=2 and e.nombre='Finalizada' and c.id_numero_estrellas is null c. and id_usuario = 2;


usuario = {
    "edad": 3,
    "nombre": "ene"
}


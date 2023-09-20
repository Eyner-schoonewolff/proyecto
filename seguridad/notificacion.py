from db.database import *
from flask import session
from typing import Dict
from psycopg2 import extras
import json
from datetime import date, time
from typing import List


class Noticacion():
    def __init__(self) -> None:
        pass

    def convertir_a_formato_json(self, resultados):
        informacion = []

        for row in resultados:
            data = {}
            for key, value in row.items():
                if isinstance(value, date):
                    data[key] = value.isoformat()
                elif isinstance(value, time):
                    data[key] = value.isoformat()
                else:
                    data[key] = value
            informacion.append(data)

        return json.dumps(informacion)

    def informacion_contratista(self,id)->List:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
                    SELECT
                        s.id,
                        s.horario AS fecha,
                        s.hora,
                        udp.nombre_completo AS nombre,
                        o.nombre AS ocupacion,
                        CASE
                            WHEN EXTRACT(DAY FROM (NOW() - s.fecha_insercion)) = 1 THEN EXTRACT(DAY FROM (NOW() - s.fecha_insercion))   || ' día'
                            WHEN EXTRACT(DAY FROM (NOW() - s.fecha_insercion)) > 0 THEN EXTRACT(DAY FROM (NOW() - s.fecha_insercion))   || ' días'
                            WHEN EXTRACT(HOUR FROM (NOW() - s.fecha_insercion)) > 0 THEN EXTRACT(HOUR FROM (NOW() - s.fecha_insercion)) || ' horas'
                            WHEN EXTRACT(HOUR FROM (NOW() - s.fecha_insercion)) <= 0 THEN EXTRACT(MINUTE FROM (NOW() - s.fecha_insercion)) || ' minutos'
                            ELSE EXTRACT(MONTH FROM (NOW() - s.fecha_insercion)) || ' semanas'
                        END AS tiempo_transcurrido
                        FROM solicitud s
                        JOIN usuarios u ON u.id = s.id_usuario_cliente
                        JOIN usuario_datos_personales udp ON udp.id = u.id_usuario_datos_personales
                        JOIN ocupacion o ON o.id = s.id_ocupacion_solicitud
                        WHERE s.id_usuario_contratista = %s
                        ORDER BY s.id ASC;
                         """
        
        cursor.execute(query, (id,))
        convertir_json = self.convertir_a_formato_json(cursor.fetchall())
        diccionario_notificacion=json.loads(convertir_json)
        return diccionario_notificacion
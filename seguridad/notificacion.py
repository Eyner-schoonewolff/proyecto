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
        row:dict

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

    def obtener_notificaciones_contratista(self,id)->List:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
                    SELECT n.id, n.titulo, n.contenido,n.leido,n.estado,CURRENT_DATE as fecha,
                        CASE
                            WHEN EXTRACT(DAY FROM (NOW() - n.fecha_creacion)) = 1 THEN EXTRACT(DAY FROM (NOW() - n.fecha_creacion))   || ' día'
                            WHEN EXTRACT(DAY FROM (NOW() - n.fecha_creacion)) > 0 THEN EXTRACT(DAY FROM (NOW() - n.fecha_creacion))   || ' días'
                            WHEN EXTRACT(HOUR FROM (NOW() - n.fecha_creacion)) > 0 THEN EXTRACT(HOUR FROM (NOW() - n.fecha_creacion)) || ' horas'
                            WHEN EXTRACT(HOUR FROM (NOW() - n.fecha_creacion)) <= 0 THEN EXTRACT(MINUTE FROM (NOW() - n.fecha_creacion)) || ' minutos'
                            ELSE EXTRACT(MONTH FROM (NOW() - n.fecha_creacion)) || ' semanas'
                        END AS tiempo_transcurrido
                        FROM notificacion n
                        WHERE n.id_usuario = %s and n.estado = false
                        ORDER BY n.id DESC;
                         """
        
        cursor.execute(query, (id,))
        convertir_json = self.convertir_a_formato_json(cursor.fetchall())
        diccionario_notificacion = json.loads(convertir_json)
        return diccionario_notificacion

    def eliminar_notificacion(self,id_notificacion)->bool:
        cursor = db.connection.cursor()
        query = 'UPDATE notificacion SET estado = TRUE WHERE id = %s'
        # cursor.execute(query,(id_notificacion,))
        # db.connection.commit()
        # cursor.close()
        return True

    
    def cambiar_estado(self,id_notificacion)->bool:
        cursor = db.connection.cursor()

        query='SELECT n.leido FROM notificacion n WHERE id = %s'
        cursor.execute(query, (id_notificacion,))
        notificacion_activa = cursor.fetchone()[0]

        if notificacion_activa:
            query = 'UPDATE notificacion SET leido = FALSE WHERE id = %s'
            notificacion = False
        else:
            query = 'UPDATE notificacion SET leido = TRUE WHERE id = %s'
            notificacion = True

        cursor.execute(query, (id_notificacion,))
        db.connection.commit()
        cursor.close()
        return notificacion

    def cantidad_notificaciones(self,id_usuario):
        cursor = db.connection.cursor()

        query = """
            SELECT count(n.id) as notificaciones
                FROM notificacion n
                 WHERE n.id_usuario = %s and n.leido = false and n.estado = false
        """

        cursor.execute(query,(id_usuario,))
        return cursor.fetchone()
        
 
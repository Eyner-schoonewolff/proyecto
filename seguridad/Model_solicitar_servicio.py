from flask import session
from db.database import *
from typing import Dict
import datetime
from psycopg2 import extras
import json
from psycopg2 import extras
from datetime import datetime, date, time


class Solicitar:
    def __init__(self, fecha="", hora="", contratista="", tipo_contratista="", evidencia="",
                 problema="", id_estado="", id_solicitud="", id_usuario: int = "") -> None:
        self.fecha = fecha
        self.hora = hora
        self.contratista = contratista
        self.tipo_contratista = tipo_contratista
        self.evidencia = evidencia
        self.problema = problema
        self.id_estado = id_estado
        self.id_solicitud = id_solicitud
        self.id_usuario = id_usuario

    def custom_json_serializer(self, obj):
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        else:
            return str(obj)

    # agregar solicitud

    def agregar(self) -> bool:
        cursor = db.connection.cursor()

        segundo = datetime.datetime.now()
        hora = self.hora+':'+repr(segundo.second)

        informacion = (self.contratista, self.id_usuario, self.tipo_contratista, self.fecha, hora, self.evidencia,
                       self.problema)

        query_informacion = """
                    INSERT INTO solicitud 
                    (id_usuario_contratista,id_usuario_cliente,id_ocupacion_solicitud,horario,hora,evidencia,descripcion,id_estado)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,1)
                """
        cursor.execute(query_informacion, informacion)
        db.connection.commit()

        return True

    # eliminar solicitud

    def eliminar(self, id) -> bool:
        cursor = db.connection.cursor()
        valor_id = (id,)
        query = 'UPDATE solicitud SET id_estado = 3 WHERE id = %s'
        cursor.execute(query, valor_id)
        db.connection.commit()
        cursor.close()
        return True

    # Clase administrador
    # Query para obtener todas las consultas del contratista

    def admin_contratista(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
            SELECT s.id, MAX(udp.nombre_completo) as nombre, MAX(s.horario) as horario, MAX(e.nombre) as estado, MAX(udp.direccion) as direccion
                FROM solicitud s
                INNER JOIN usuarios u ON s.id_usuario_cliente = u.id
                INNER JOIN usuario_ocupaciones uo ON s.id_usuario_contratista = uo.id_usuario
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales = udp.id
                INNER JOIN estado e ON s.id_estado = e.id
                GROUP BY s.id
         """
        cursor.execute(query)
        return cursor.fetchall()

    # Clase administrador
    # Query para obtener las consultas del cliente

    def admin_cliente(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
              SELECT s.id, MAX(s.horario) as horario,MAX(e.nombre) as estado, MAX(o.nombre) as ocupacion, MAX(udp.nombre_completo) as nombre
                FROM solicitud s
                INNER JOIN usuarios u ON s.id_usuario_contratista=u.id
                INNER JOIN ocupacion o ON s.id_ocupacion_solicitud=o.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                INNER JOIN estado e ON s.id_estado=e.id
                GROUP BY s.id;
         """
        cursor.execute(query)
        return cursor.fetchall()

    def contratista_(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
             SELECT s.id, MAX(udp.nombre_completo) nombre, MAX(udp.numero_celular) numero, MAX(s.horario) as horario, MAX(s.hora) as hora, MAX(e.nombre) as estado, MAX(s.evidencia) as evidencia, MAX(s.descripcion) as descripcion, MAX(udp.direccion) as direccion
               FROM solicitud s
               INNER JOIN usuarios u ON s.id_usuario_cliente=u.id
               INNER JOIN usuario_ocupaciones uo ON s.id_usuario_contratista=uo.id_usuario
               INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales = udp.id
               INNER JOIN estado e ON s.id_estado = e.id
               LEFT JOIN calificacion c ON c.id_solicitud=s.id
               WHERE s.id_usuario_contratista=%s and id_numero_estrellas is null 
               GROUP BY s.id;
         """
        cursor.execute(query, (self.id_usuario,))
        result = cursor.fetchall()
        json_result = json.dumps(result, default=self.custom_json_serializer)

        return json_result

    def cliente(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
           SELECT s.id,  MAX(s.horario) as horario, MAX(e.nombre) as estado, MAX(s.id_ocupacion_solicitud), MAX(o.nombre) as ocupacion,  MAX(udp.nombre_completo) as nombre,  MAX(udp.numero_celular) as numero
                FROM solicitud s
                INNER JOIN usuarios u ON s.id_usuario_contratista=u.id
                INNER JOIN ocupacion o ON s.id_ocupacion_solicitud=o.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                INNER JOIN estado e ON s.id_estado=e.id
                LEFT JOIN calificacion c ON c.id_solicitud=s.id
                WHERE s.id_usuario_cliente=%s and c.id_numero_estrellas is null 
                GROUP BY s.id;
         """

        cursor.execute(query, (self.id_usuario,))
        return cursor.fetchall()

        # cambiar query 5
    def consultar_contratista(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
               SELECT MAX(uo.id_usuario) as id,udp.nombre_completo as nombre,MAX(o.nombre) as ocupacion
                  FROM usuario_ocupaciones uo
                  INNER JOIN usuarios u ON uo.id_usuario=u.id
                  INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                  INNER JOIN ocupacion o ON uo.id_ocupacion= o.id
                  WHERE uo.id_ocupacion=%s and uo.eliminado=0
                  GROUP BY udp.nombre_completo
        """
        cursor.execute(query, (self.id_solicitud,))
        return cursor.fetchall()

    def evidencia_(self, id) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = "SELECT descripcion,evidencia FROM solicitud WHERE id=%s "
        cursor.execute(query, (id,))
        return cursor.fetchone()

    def actualizar_estado(self):
        cursor = db.connection.cursor()
        informacion = (self.id_estado, self.id_solicitud)
        query = 'UPDATE solicitud SET id_estado = %s WHERE id = %s'
        cursor.execute(query, informacion)
        db.connection.commit()

        return None

    def actualizar_fecha_estado(self):
        cursor = db.connection.cursor()
        informacion = (self.id_estado, self.fecha,
                       self.hora, self.id_solicitud)
        query = 'UPDATE solicitud SET id_estado = %s,horario=%s,hora=%s WHERE id = %s'
        cursor.execute(query, informacion)
        db.connection.commit()

        return None

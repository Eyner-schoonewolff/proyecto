from flask import jsonify
from db.database import *
from typing import Dict
import datetime
from psycopg2 import extras
import json
from psycopg2 import extras
from datetime import date, time
import datetime
from functools import partial


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

    def agregar(self) -> bool:
        cursor = db.connection.cursor()
        segundo = datetime.datetime.now()

        if self.hora is not None:
            hora = self.hora + ':' + str(segundo.second)
        else:
            hora = str(segundo.second)

        informacion = (self.contratista, self.id_usuario, self.tipo_contratista,
                       self.fecha, hora, self.evidencia, self.problema)

        query_informacion = """
                    INSERT INTO solicitud 
                    (id_usuario_contratista, id_usuario_cliente, id_ocupacion_solicitud, horario, hora, evidencia, descripcion, id_estado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
                """
        cursor.execute(query_informacion, informacion)
        db.connection.commit()

        return True

    # eliminar solicitud

    def cancelar(self, id) -> bool:
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
               WHERE s.id_usuario_contratista=%s
               GROUP BY s.id;
         """
        cursor.execute(query, (self.id_usuario,))
        result = cursor.fetchall()

        convertir_json = self.convertir_a_formato_json(result)
        return convertir_json

    def contratista_calificar(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
     SELECT s.id,  s.horario as horario, e.nombre as estado,
       s.id_ocupacion_solicitud as id_ocupacion, o.nombre as ocupacion,
       udp.nombre_completo as nombre, udp.numero_celular as numero, udp.direccion as direccion
            FROM solicitud s
            INNER JOIN usuarios u ON s.id_usuario_contratista = u.id
            INNER JOIN ocupacion o ON s.id_ocupacion_solicitud = o.id
            INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales = udp.id
            INNER JOIN estado e ON s.id_estado = e.id
            LEFT JOIN (
                SELECT id_solicitud, id_numero_estrellas
                FROM calificacion
                WHERE id_usuario = %s
            ) c ON c.id_solicitud = s.id
            WHERE s.id_usuario_cliente = %s AND e.nombre = 'Finalizada' and c.id_numero_estrellas is null;
         """
        cursor.execute(query, (self.id_usuario, self.id_usuario,))
        result = cursor.fetchall()

        convertir_json = self.convertir_a_formato_json(result)
        return convertir_json

    def cliente_calificar(self):
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
             SELECT s.id, udp.nombre_completo as nombre, udp.numero_celular numero, s.horario as horario, s.hora as hora, e.nombre as estado, s.evidencia as evidencia, s.descripcion as descripcion, udp.direccion as direccion, c.id_numero_estrellas as estrellas
                FROM solicitud s
                INNER JOIN usuarios u ON s.id_usuario_cliente=u.id
                INNER JOIN usuario_ocupaciones uo ON s.id_usuario_contratista=uo.id_usuario
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales = udp.id
                INNER JOIN estado e ON s.id_estado = e.id
                LEFT JOIN (
                    SELECT id_solicitud, id_numero_estrellas
                    FROM calificacion
                    WHERE id_usuario = %s
                ) c ON c.id_solicitud = s.id
                WHERE s.id_usuario_contratista=%s AND e.nombre = 'Finalizada' and c.id_numero_estrellas is null
                GROUP BY s.id, udp.nombre_completo, udp.numero_celular, s.horario, s.hora, e.nombre, s.evidencia, s.descripcion, udp.direccion, c.id_numero_estrellas;
         """
        cursor.execute(query, (self.id_usuario, self.id_usuario,))
        resultos = cursor.fetchall()

        resultado_json = self.convertir_a_formato_json(resultos)
        return resultado_json

    def cliente(self):
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
             SELECT s.id,  MAX(s.horario) as horario,MAX(s.hora) as hora, MAX(e.nombre) as estado, MAX(s.id_ocupacion_solicitud) as id_ocupacion, MAX(o.nombre) as ocupacion,  MAX(udp.nombre_completo) as nombre,  MAX(udp.numero_celular) as numero
                FROM solicitud s
                INNER JOIN usuarios u ON s.id_usuario_contratista=u.id
                INNER JOIN ocupacion o ON s.id_ocupacion_solicitud=o.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                INNER JOIN estado e ON s.id_estado=e.id
                LEFT JOIN calificacion c ON c.id_solicitud=s.id
                WHERE s.id_usuario_cliente=%s
                GROUP BY s.id;
         """

        cursor.execute(query, (self.id_usuario,))
        resultos = cursor.fetchall()

        resultado_json = self.convertir_a_formato_json(resultos)
        return resultado_json

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
                  GROUP BY udp.nombre_completo;
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

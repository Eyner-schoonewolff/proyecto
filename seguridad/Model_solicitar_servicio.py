from flask import session
from db.database import *
from typing import Dict
import datetime


class Solicitar:
    def __init__(self, fecha="", hora="", contratista="", tipo_contratista="", evidencia="", 
                 problema="",id_estado="",id_solicitud="") -> None:
        self.fecha = fecha
        self.hora = hora
        self.contratista = contratista
        self.tipo_contratista = tipo_contratista
        self.evidencia = evidencia
        self.problema = problema
        self.id_estado = id_estado
        self.id_solicitud = id_solicitud
        self.id_usuario = session.get('id')

    def agregar(self) -> bool:
        cursor = db.connection.cursor()

        segundo = datetime.datetime.now()
        hora=self.hora+':'+repr(segundo.second)

        informacion = (self.contratista, self.id_usuario, self.tipo_contratista, self.fecha,hora, self.evidencia,
                       self.problema)

        query_informacion = """
                    INSERT INTO solicitud 
                    (id_usuario_contratista,id_usuario_cliente,id_ocupacion_solicitud,horario,hora,evidencia,descripcion,id_estado)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,1)
                """
        cursor.execute(query_informacion, informacion)
        db.connection.commit()

        return True

    def eliminar(self, id) -> bool:
        cursor = db.connection.cursor()
        valor_id = (id,)
        query = 'UPDATE solicitud SET id_estado = 3 WHERE id = %s'
        cursor.execute(query, valor_id)
        db.connection.commit()
        cursor.close()
        return True

    def admin_contratista(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
            SELECT s.id,udp.nombre_completo nombre,s.horario,e.nombre estado,udp.direccion
               FROM solicitud s
               INNER JOIN usuarios u ON s.id_usuario_cliente=u.id
               INNER JOIN usuario_ocupaciones uo ON s.id_usuario_contratista=uo.id_usuario
               INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales = udp.id
               INNER JOIN estado e ON s.id_estado = e.id
               GROUP BY s.id;
         """
        cursor.execute(query)
        return cursor.fetchall()

    def admin_cliente(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
              SELECT s.id, s.horario, e.nombre estado, o.nombre ocupacion, udp.nombre_completo nombre
                FROM solicitud s
                INNER JOIN usuarios u ON s.id_usuario_contratista=u.id
                INNER JOIN ocupacion o ON s.`id_ocupacion_solicitud`=o.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                INNER JOIN estado e ON s.id_estado=e.id
                GROUP BY s.id;
         """
        cursor.execute(query)
        return cursor.fetchall()

    def contratista_(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
             SELECT s.id,udp.nombre_completo nombre,udp.numero_celular numero,s.horario,s.hora,e.nombre estado,s.evidencia,s.descripcion,udp.direccion
               FROM solicitud s
               INNER JOIN usuarios u ON s.id_usuario_cliente=u.id
               INNER JOIN usuario_ocupaciones uo ON s.id_usuario_contratista=uo.id_usuario
               INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales = udp.id
               INNER JOIN estado e ON s.id_estado = e.id
               LEFT JOIN calificacion c ON c.`id_solicitud`=s.id
               WHERE s.id_usuario_contratista=%s and numero_estrellas is null 
               GROUP BY s.id;
         """
        cursor.execute(query, (self.id_usuario,))
        return cursor.fetchall()

    def cliente(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
           SELECT s.id, s.horario, e.nombre estado, s.id_ocupacion_solicitud, o.nombre ocupacion, udp.nombre_completo nombre, udp.numero_celular numero
                FROM solicitud s
                INNER JOIN usuarios u ON s.id_usuario_contratista=u.id
                INNER JOIN ocupacion o ON s.`id_ocupacion_solicitud`=o.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                INNER JOIN estado e ON s.id_estado=e.id
                LEFT JOIN calificacion c ON c.`id_solicitud`=s.id
                WHERE s.id_usuario_cliente=%s and c.numero_estrellas is null 
                GROUP BY s.id;
         """

        cursor.execute(query, (self.id_usuario,))
        return cursor.fetchall()

        # cambiar query 5
    def consultar_contratista(self, id_ocupacion) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
               SELECT uo.id_usuario id,udp.nombre_completo nombre,o.nombre AS ocupacion
                  FROM usuario_ocupaciones uo
                  INNER JOIN usuarios u ON uo.id_usuario=u.id
                  INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                  INNER JOIN ocupacion o ON uo.id_ocupacion= o.id
                  WHERE uo.id_ocupacion=%s
                  GROUP BY udp.nombre_completo
        """
        cursor.execute(query, (id_ocupacion,))
        return cursor.fetchall()

    def evidencia_(self, id) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = "SELECT descripcion,evidencia FROM solicitud WHERE id=%s "
        cursor.execute(query, (id,))
        return cursor.fetchone()

    def actualizar_estado(self):
        cursor = db.connection.cursor()
        informacion = (self.id_estado,self.fecha,self.hora,self.id_solicitud)
        query = 'UPDATE solicitud SET id_estado = %s,horario=%s,hora=%s WHERE id = %s'
        cursor.execute(query, informacion)
        db.connection.commit()

        return True

        # cambiar query 6
    def ultima_solicitud(self):
        cursor = db.connection.cursor(dictionary=True)
        query = """
            SELECT id_usuario_contratista id,udp.nombre_completo nombre
                FROM solicitud s
                INNER JOIN usuarios u ON s.`id_usuario_cliente` = u.`id`
                INNER JOIN usuario_datos_personales udp ON u.`id_usuario_datos_personales`= udp.id
                ORDER BY s.id DESC
                LIMIT 1;
        """
        cursor.execute(query)
        return cursor.fetchone()

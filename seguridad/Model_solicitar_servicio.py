from flask import session
from db.database import *
from typing import Dict
import datetime


class Solicitar:
    def __init__(self, fecha="", hora="", tipo_contratista="", contratista="", evidencia="", problema="") -> None:
        self.fecha = fecha
        self.hora = hora
        self.tipo_contratista = tipo_contratista
        self.contratista = contratista
        self.evidencia = evidencia
        self.problema = problema
        self.id_usuario = session.get('id')

    def agregar(self) -> bool:
        cursor = db.connection.cursor()

        segundo = datetime.datetime.now()
        fechatime = self.fecha + ' ' + self.hora+':'+repr(segundo.second)
        informacion = (self.contratista, self.tipo_contratista, fechatime, self.evidencia,
                       self.problema, self.id_usuario)

        query_informacion = """
                    INSERT INTO solicitud (id_usuario_contratista,id_ocupacion,horario,evidencia,descripcion,id_usuario_cliente,id_estado)
                    VALUES (%s,%s,%s,%s,%s,%s,1)
                """
        cursor.execute(query_informacion, informacion)
        db.connection.commit()

        return True

    def eliminar(self, id) -> bool:
        cursor = db.connection.cursor()
        valor_id = (id,)
        query='UPDATE solicitud SET id_estado = 4 WHERE id = %s'
        cursor.execute(query,valor_id)
        db.connection.commit()
        cursor.close()
        return True

    def contratista_(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
            SELECT s.id,udp.nombre_completo nombre,udp.numero_celular numero,s.horario,e.nombre estado,s.evidencia,s.descripcion,udp.direccion
               FROM solicitud s
               INNER JOIN usuarios u ON s.id_usuario_cliente=u.id
               INNER JOIN usuario_ocupaciones uo ON s.id_usuario_contratista=uo.id_usuario
               INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales = udp.id
               INNER JOIN estado e ON s.id_estado = e.id
               WHERE s.id_usuario_contratista=%s
               GROUP BY s.id;
         """
        cursor.execute(query, (self.id_usuario,))
        return cursor.fetchall()

    def cliente(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
                SELECT s.id, s.horario, e.nombre estado, s.id_ocupacion, o.nombre as ocupacion, udp.nombre_completo nombre, udp.numero_celular numero
                FROM solicitud s
                INNER JOIN usuario_ocupaciones uo1 ON s.id_ocupacion = uo1.id_ocupacion
                INNER JOIN ocupacion o ON uo1.id_ocupacion = o.id
                INNER JOIN usuario_ocupaciones uo2 ON s.id_usuario_contratista = uo2.id_usuario
                INNER JOIN usuarios u ON uo2.id_usuario = u.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales = udp.id
                INNER JOIN estado e ON s.id_estado = e.id
                WHERE id_usuario_cliente = %s
                GROUP BY s.id;
         """

        cursor.execute(query, (self.id_usuario,))
        return cursor.fetchall()

    def consultar_contratista(self, id_ocupacion) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
               SELECT uo.id_usuario id,udp.nombre_completo nombre,o.nombre AS ocupacion
                  FROM usuario_ocupaciones uo
                  INNER JOIN usuarios u ON uo.id_usuario=u.id
                  INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                  INNER JOIN ocupacion o ON uo.id_ocupacion= o.id
                  WHERE uo.id_ocupacion=%s
        """
        cursor.execute(query, (id_ocupacion,))
        return cursor.fetchall()

    def evidencia_(self, id) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = "SELECT descripcion,evidencia FROM solicitud WHERE id=%s "
        cursor.execute(query, (id,))
        return cursor.fetchone()

    def actualizar_estado(self,id_estado,id_solicitud):
        cursor = db.connection.cursor()
        informacion = (id_estado,id_solicitud)
        query = 'UPDATE solicitud SET id_estado = %s WHERE id = %s'
        cursor.execute(query, informacion)
        db.connection.commit()
        cursor.close()

        return f"registro(s) actualizado(s)"
    
    def ultima_solicitud(self):
        cursor=db.connection.cursor(dictionary=True)
        query="""
            SELECT id_usuario_contratista id,udp.nombre_completo nombre
                FROM solicitud s
                INNER JOIN usuarios u ON s.`id_usuario_cliente` = u.`id`
                INNER JOIN usuario_datos_personales udp ON u.`id_usuario_datos_personales`= udp.id
                ORDER BY s.id DESC
                LIMIT 1;
        """
        cursor.execute(query)
        return cursor.fetchone()
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

    def agregar(self) -> None:
        cursor = db.connection.cursor()

        segundo = datetime.datetime.now()
        fechatime = self.fecha + ' ' + self.hora+':'+repr(segundo.second)
        informacion = (self.contratista, fechatime, self.evidencia,
                       self.problema, self.id_usuario)

        query_informacion = """
                    INSERT INTO solicitud (id_usuario_ocupaciones,horario,evidencia,descripcion,id_usuario_cliente)
                    VALUES (%s,%s,%s,%s,%s)
                """
        cursor.execute(query_informacion,informacion)
        db.connection.commit()

        return '1'

    def eliminar(self, id) -> bool:
        cursor = db.connection.cursor()
        query = "DELETE FROM solicitud WHERE id = %s"
        valores = (id,)
        cursor.execute(query, valores)
        db.connection.commit()
        return True

    def contratista_(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
               SELECT udp.nombre_completo nombre,udp.numero_celular numero,s.horario,s.estado,s.evidencia,s.descripcion,udp.direccion
               FROM solicitud s
               INNER JOIN usuarios u ON s.id_usuario_cliente=u.id
               INNER JOIN usuario_ocupaciones uo ON s.id_usuario_ocupaciones=uo.id

               INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales = udp.id
               WHERE uo.id_usuario=%s
         
         """
        cursor.execute(query, (self.id_usuario,))
        return cursor.fetchall()

    def cliente(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
            SELECT udp.nombre_completo nombre,udp.numero_celular numero,s.horario,o.nombre ocupacion,s.estado,s.id
                  FROM usuario_ocupaciones uo
                  INNER JOIN usuarios u ON uo.`id_usuario`=u.`id`
                  INNER JOIN usuario_datos_personales udp ON u.`id_usuario_datos_personales`=udp.`id` 
                  INNER JOIN ocupacion o ON uo.`id_ocupacion`= o.`id`
                  INNER JOIN solicitud s ON s.id_usuario_ocupaciones=uo.`id`
                  WHERE s.id_usuario_cliente=%s
         
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
    
    def consultar_contratista_albanil(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
                SELECT uo.id_usuario id,udp.nombre_completo nombre
                  FROM usuario_ocupaciones uo
                  INNER JOIN usuarios u ON uo.id_usuario=u.id
                  INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                  WHERE uo.id_ocupacion=1
        """
        cursor.execute(query)
        return cursor.fetchone()

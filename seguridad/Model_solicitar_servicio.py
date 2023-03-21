from flask import session
from db.database import *
from typing import Dict
import datetime


class solicitar:
    def __init__(self,fecha="", hora="", tipo_contratista="", contratista="", problema="") -> None:
        self.fecha = fecha
        self.hora = hora
        self.tipo_contratista = tipo_contratista
        self.contratista = contratista
        self.problema = problema
        self.id_usuario = session.get('id')

    def agregar(self, id_user) -> None:
        segundo = datetime.datetime.now()
        fechatime = self.fecha + ' ' + self.hora+':'+repr(segundo.second)
        cursor = db.connection.cursor()
        informacion = (self.contratista, fechatime, self.problema, id_user)
        query_informacion = """
                    INSERT INTO solicitud (id_usuario_ocupaciones,horario,descripcion,id_usuario_cliente)
                    VALUES (%s,%s,%s,%s)
                """
        cursor.execute(query_informacion, (informacion))
        db.connection.commit()
        return '1'

    def eliminar(self):
        pass

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
            SELECT udp.nombre_completo nombre,udp.numero_celular numero,s.horario,o.nombre ocupacion,s.estado
                  FROM usuario_ocupaciones uo
                  INNER JOIN usuarios u ON uo.`id_usuario`=u.`id`
                  INNER JOIN usuario_datos_personales udp ON u.`id_usuario_datos_personales`=udp.`id` 
                  INNER JOIN ocupacion o ON uo.`id_ocupacion`= o.`id`
                  INNER JOIN solicitud s ON s.id_usuario_ocupaciones=uo.`id`
                  WHERE s.id_usuario_cliente=%s
         
         """
        cursor.execute(query, (self.id_usuario,))
        return cursor.fetchall()

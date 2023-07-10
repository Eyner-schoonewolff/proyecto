from db.database import *
from flask import session
from typing import Dict
from psycopg2 import extras


class Perfiles:
    def __init__(self, id_usuario_cliente="", id_usuario="") -> None:
        self.tipo_usuario = session.get('tipo_usuario')
        self.id_usuario_cliente = id_usuario_cliente
        self.id_usuario = id_usuario

    # clase calificacion
    def consulta_cliente(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
            SELECT u.id, udp.nombre_completo nombre, MAX(c.id_numero_estrellas) as calificacion, MAX(c.observaciones) as comentario, MAX(c.registro) as dia_calificacion
            FROM calificacion c
            INNER JOIN solicitud s ON c.id_solicitud = s.id
            INNER JOIN usuarios u ON s.id_usuario_cliente = u.id
            INNER JOIN tipo_usuario tu ON u.id_tipo_usuario = tu.id
            INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales = udp.id
            GROUP BY u.id, udp.nombre_completo
        """
        cursor.execute(query)
        return cursor.fetchall()

    # clase calificacion
    def consulta_contratista(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
            SELECT u.id,udp.nombre_completo nombre, MAX(c.id_numero_estrellas) as calificacion, MAX(c.observaciones) as comentario, MAX(c.registro) as dia_calificacion
                FROM calificacion c
                INNER JOIN solicitud s ON c.id_solicitud=s.id
                INNER JOIN usuarios u ON s.id_usuario_contratista=u.id
                INNER JOIN tipo_usuario tu ON u.id_tipo_usuario=tu.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                GROUP BY u.id, udp.nombre_completo
        """
        cursor.execute(query)
        return cursor.fetchall()

    # clase calificacion
    def calificaciones_cliente(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        valores = (self.id_usuario_cliente, self.id_usuario)
        query = """
            SELECT udp.nombre_completo nombre, c.id_numero_estrellas valor, c.observaciones comentario,c.registro 
                FROM calificacion c
                INNER JOIN solicitud s ON c.id_solicitud=s.id
                INNER JOIN usuarios u ON s.id_usuario_contratista=u.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                WHERE s.id_usuario_cliente= %s and c.id_usuario!= %s
        """
        cursor.execute(query, valores)
        return cursor.fetchall()

    def calificaciones_contratista(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        valores = (self.id_usuario_cliente, self.id_usuario)
        query = """
            SELECT udp.nombre_completo nombre, c.id_numero_estrellas valor, c.observaciones comentario,c.registro 
                FROM calificacion c
                INNER JOIN solicitud s ON c.id_solicitud=s.id
                INNER JOIN usuarios u ON s.id_usuario_cliente=u.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                WHERE s.id_usuario_contratista= %s and c.id_usuario!= %s
        """
        cursor.execute(query, valores)
        return cursor.fetchall()

    def promedio_cliente(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        valores = (self.id_usuario_cliente, self.id_usuario)
        query = """
              SELECT ROUND(SUM(c.id_numero_estrellas) / COUNT(c.id_numero_estrellas), 1) as promedio
                FROM calificacion c
                INNER JOIN solicitud s ON c.id_solicitud = s.id
                INNER JOIN usuarios u ON s.id_usuario_contratista = u.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales = udp.id
                WHERE s.id_usuario_cliente = %s AND c.id_usuario <> %s
         """

        cursor.execute(query, valores)
        return cursor.fetchone()

    def promedio_contratista(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        valores = (self.id_usuario_cliente, self.id_usuario)
        query = """
            SELECT ROUND(SUM(c.id_numero_estrellas) / COUNT(c.id_numero_estrellas), 1) as promedio
                FROM calificacion c
                INNER JOIN solicitud s ON c.id_solicitud = s.id
                INNER JOIN usuarios u ON s.id_usuario_cliente = u.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales = udp.id
                WHERE s.id_usuario_contratista = %s AND c.id_usuario <> %s
        """
        cursor.execute(query, valores)
        return cursor.fetchone()

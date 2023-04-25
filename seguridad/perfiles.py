from db.database import *
from flask import session
from typing import Dict

class Perfiles:
    def __init__(self,id_usuario_cliente="",id_usuario="") -> None:
        self.tipo_usuario = session.get('tipo_usuario')
        self.id_usuario_cliente=id_usuario_cliente
        self.id_usuario=id_usuario

    def consulta_cliente(self)->Dict:
        cursor=db.connection.cursor(dictionary=True)
        query="""
            SELECT u.id,udp.`nombre_completo` nombre, c.`numero_estrellas` calificacion, c.`observaciones` comentario,c.registro dia_calificacion
                FROM calificacion c
                INNER JOIN solicitud s ON c.id_solicitud=s.`id`
                INNER JOIN usuarios u ON s.`id_usuario_cliente`=u.id
                INNER JOIN `tipo_usuario` tu ON u.`id_tipo_usuario`=tu.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                GROUP BY udp.nombre_completo
        """
        cursor.execute(query)
        return cursor.fetchall()
    
    def consulta_contratista(self)->Dict:
        cursor=db.connection.cursor(dictionary=True)
        query="""
            SELECT u.id,udp.`nombre_completo` nombre, c.`numero_estrellas` calificacion, c.`observaciones` comentario,c.registro dia_calificacion
                FROM calificacion c
                INNER JOIN solicitud s ON c.id_solicitud=s.`id`
                INNER JOIN usuarios u ON s.id_usuario_contratista=u.id
                INNER JOIN `tipo_usuario` tu ON u.`id_tipo_usuario`=tu.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                GROUP BY udp.nombre_completo
        """
        cursor.execute(query)
        return cursor.fetchall()
    
    def calificaciones_cliente(self)->Dict:
        cursor=db.connection.cursor(dictionary=True)
        valores=(self.id_usuario_cliente,self.id_usuario)
        query="""
            SELECT udp.`nombre_completo` nombre, c.`numero_estrellas` valor, c.`observaciones` comentario,c.`registro` 
                FROM calificacion c
                INNER JOIN solicitud s ON c.id_solicitud=s.id
                INNER JOIN usuarios u ON s.`id_usuario_contratista`=u.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                WHERE s.`id_usuario_cliente`= %s and c.`id_usuario`!= %s
        """
        cursor.execute(query,valores)
        return cursor.fetchall()
    
    def calificaciones_contratista(self)->Dict:
        cursor=db.connection.cursor(dictionary=True)
        valores=(self.id_usuario_cliente,self.id_usuario)
        query="""
            SELECT udp.`nombre_completo` nombre, c.`numero_estrellas` valor, c.`observaciones` comentario,c.`registro` 
                FROM calificacion c
                INNER JOIN solicitud s ON c.id_solicitud=s.id
                INNER JOIN usuarios u ON s.`id_usuario_cliente`=u.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                WHERE s.`id_usuario_contratista`= %s and c.`id_usuario`!= %s
        """
        cursor.execute(query,valores)
        return cursor.fetchall()
    
    def promedio_cliente(self)->Dict:
        cursor=db.connection.cursor(dictionary=True)
        valores=(self.id_usuario_cliente,self.id_usuario)
        query="""
            SELECT udp.`nombre_completo` nombre, ROUND(SUM(c.`numero_estrellas`) / COUNT(c.`numero_estrellas`), 1) as promedio
                FROM calificacion c
                INNER JOIN solicitud s ON c.id_solicitud=s.id
                INNER JOIN usuarios u ON s.`id_usuario_contratista`=u.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                WHERE s.`id_usuario_cliente`=%s and c.`id_usuario`!= %s
        """
        cursor.execute(query,valores)
        return cursor.fetchone()
    
    def promedio_contratista(self)->Dict:
        cursor=db.connection.cursor(dictionary=True)
        valores=(self.id_usuario_cliente,self.id_usuario)
        query="""
            SELECT udp.`nombre_completo` nombre, ROUND(SUM(c.`numero_estrellas`) / COUNT(c.`numero_estrellas`), 1) as promedio
                FROM calificacion c
                INNER JOIN solicitud s ON c.id_solicitud=s.id
                INNER JOIN usuarios u ON s.`id_usuario_cliente`=u.id
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                WHERE s.`id_usuario_contratista`=%s and c.`id_usuario`!= %s
        """
        cursor.execute(query,valores)
        return cursor.fetchone()
        
        

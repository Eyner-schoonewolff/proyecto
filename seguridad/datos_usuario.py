from db.database import *
from typing import Dict
from flask import session


class DatosUsuario:
    def __init__(self) -> None:
        pass

    def ocupaciones(self):
        cursor = db.connection.cursor(dictionary=True)
        query = "SELECT id,nombre ocupacion FROM ocupacion o"
        cursor.execute(query)
        return cursor.fetchall()

    def verificar_existe_ocupacion(self):
        cursor = db.connection.cursor(dictionary=True)
        id = session.get('id')
        query = """
            SELECT o.nombre ocupacion ,uo.id_ocupacion
                        FROM usuario_ocupaciones uo
                        INNER JOIN usuarios u ON uo.`id_usuario`= u.id
                        INNER JOIN ocupacion o ON uo.`id_ocupacion`=o.`id`
                        WHERE u.id = %s
        """
        cursor.execute(query, (id,))
        datos = cursor.fetchall()
        if datos == []:
            return None
        return datos

    def guardar_ocupacion(self):
        ocupaciones_disponibles = []
        ocupacion_existente = self.verificar_existe_ocupacion()
        ocupaciones_guardadas = []  # Lista auxiliar para almacenar las ocupaciones ya guardadas
        if ocupacion_existente is None:
            # Si no existe ninguna ocupación, devolvemos todas las ocupaciones disponibles
            return [trabajo['ocupacion'] for trabajo in self.ocupaciones()]
        for ocupacion in ocupacion_existente:
            # Agregamos las ocupaciones ya existentes a la lista auxiliar
            ocupaciones_guardadas.append(ocupacion['ocupacion'])
        for trabajo in self.ocupaciones():
            if trabajo['ocupacion'] not in ocupaciones_guardadas:
                # Si la ocupación no está en la lista auxiliar, la agregamos a las disponibles
                ocupaciones_disponibles.append(trabajo['ocupacion'])
        return ocupaciones_disponibles

    def obtener(self) -> Dict:
        # Obtener el cursor y el correo electrónico actual
        cursor=db.connection.cursor(dictionary = True)
        id=session.get('id')

        # Consultar los datos del usuario con sus ocupaciones
        query="""
        SELECT udp.numero_celular, udp.numero_documento, udp.direccion, GROUP_CONCAT(o.nombre SEPARATOR ', ') AS ocupaciones
        FROM usuario_datos_personales udp
        INNER JOIN usuarios u ON u.id_usuario_datos_personales = udp.id
        INNER JOIN usuario_ocupaciones uo ON uo.id_usuario =u.`id`
        INNER JOIN ocupacion o ON uo.id_ocupacion = o.id
        WHERE u.id=%s
        GROUP BY udp.nombre_completo, udp.numero_celular, udp.numero_documento, udp.direccion
        """
        cursor.execute(query, (id,))
        datos=cursor.fetchone()

        # Si los datos no se encuentran, consultar solo los datos básicos del usuario
        if datos is None:
            query_="""
            SELECT udp.numero_celular, udp.numero_documento, udp.direccion
            FROM usuario_datos_personales udp
            INNER JOIN usuarios u ON u.id_usuario_datos_personales = udp.id
            WHERE u.id = %s
            """
            cursor.execute(query_, (id,))
            datos=cursor.fetchone()
            datos['ocupaciones']=None

        return datos

    def actualizar(self):
        pass

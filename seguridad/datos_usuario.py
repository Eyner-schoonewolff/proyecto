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

    def obtener(self,id) -> Dict:
        # Obtener el cursor y el correo electrónico actual
        cursor = db.connection.cursor(dictionary=True)
        # Consultar los datos del usuario con sus ocupaciones
        query = """
        SELECT udp.nombre_completo,udp.numero_celular, udp.numero_documento, udp.direccion, GROUP_CONCAT(o.nombre SEPARATOR ', ') AS ocupaciones,o.id id_ocupacion
        FROM usuario_datos_personales udp
        INNER JOIN usuarios u ON u.id_usuario_datos_personales = udp.id
        INNER JOIN usuario_ocupaciones uo ON uo.id_usuario =u.`id`
        INNER JOIN ocupacion o ON uo.id_ocupacion = o.id
        WHERE u.id=%s
        GROUP BY udp.nombre_completo, udp.numero_celular, udp.numero_documento, udp.direccion
        """
        cursor.execute(query, (id,))
        datos = cursor.fetchone()

        # Si los datos no se encuentran, consultar solo los datos básicos del usuario
        if datos is None:
            query_ = """
            SELECT udp.nombre_completo,udp.numero_celular, udp.numero_documento, udp.direccion
            FROM usuario_datos_personales udp
            INNER JOIN usuarios u ON u.id_usuario_datos_personales = udp.id
            WHERE u.id = %s
            """
            cursor.execute(query_, (id,))
            datos = cursor.fetchone()
            datos['ocupaciones'] = None

        return datos

    def actualizar(self, nombre, celular, direccion,id_usuario):
        cursor = db.connection.cursor()
        datos_actualizar=(nombre,celular,direccion,id_usuario)
        query='UPDATE usuario_datos_personales SET nombre_completo = %s, numero_celular = %s, direccion=%s WHERE id = %s'
        cursor.execute(query,datos_actualizar)
        db.connection.commit()
        cursor.close()

        return f"registro(s) actualizado(s)"

from db.database import *
from typing import Dict
from flask import session


class DatosUsuario:
    def __init__(self) -> None:
        pass

    def obtener(self) -> Dict:
        # Obtener el cursor y el correo electrónico actual
        cursor = db.connection.cursor(dictionary=True)
        email = session.get('email')

        # Consultar los datos del usuario con sus ocupaciones
        query = """
        SELECT udp.numero_celular, udp.numero_documento, udp.direccion, GROUP_CONCAT(o.nombre SEPARATOR ', ') AS ocupaciones
        FROM usuario_datos_personales udp
        INNER JOIN usuarios u ON u.id_usuario_datos_personales = udp.id
        INNER JOIN usuario_ocupaciones uo ON uo.id_usuario = udp.id
        INNER JOIN ocupacion o ON uo.id_ocupacion = o.id
        WHERE u.email = %s
        GROUP BY u.email, udp.nombre_completo, udp.numero_celular, udp.numero_documento, udp.direccion;
        """
        cursor.execute(query, (email,))
        datos = cursor.fetchone()

        # Si los datos no se encuentran, consultar solo los datos básicos del usuario
        if datos is None:
            query_ = """
            SELECT udp.numero_celular, udp.numero_documento, udp.direccion 
            FROM usuario_datos_personales udp
            INNER JOIN usuarios u ON u.id_usuario_datos_personales = udp.id    
            WHERE u.email = %s
            """
            cursor.execute(query_, (email,))
            datos = cursor.fetchone()
            datos['ocupaciones'] = None

        return datos

    def actualizar(self):
        pass

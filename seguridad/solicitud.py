from db.database import *
from typing import Dict


class ConsultarSolicitud:
    def __init__(self) -> None:
        pass

    def contratista(self, id_usuario) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
            SELECT udp.nombre_completo nombre,udp.numero_celular numero,s.horario,s.estado,s.evidencia,s.descripcion,udp.direccion
            FROM solicitud s
            INNER JOIN usuarios u ON s.id_usuario_cliente=u.id
            INNER JOIN usuario_ocupaciones uo ON s.id_usuario_ocupaciones=uo.id

            INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales = udp.id
            WHERE uo.id_usuario=%s
      
        """
        cursor.execute(query, (id_usuario,))
        return cursor.fetchall()

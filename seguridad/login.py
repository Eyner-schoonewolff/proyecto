from db.database import *
from typing import Dict


class Login:
    def __init__(self, email, contrasenia) -> None:
        self.email = email
        self.contrasenia = contrasenia
        self.usuario = self.obtener_usuario()

    def obtener_usuario(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """SELECT u.email, u.contraseña, tu.nombre tipo,udp.`nombre_completo` nombre
                FROM usuarios u
                INNER JOIN tipo_usuario tu on u.id_tipo_usuario = tu.id
                INNER JOIN usuario_datos_personales udp on u.id = udp.`id_usuario`
                WHERE u.email=%s"""
        cursor.execute(query, (self.email,))
        return cursor.fetchone()

    def verificar(self) -> bool:
        if self.usuario is None:
            return False
        # Verificar la contraseña
        if self.usuario['contraseña'] == self.contrasenia:
            return True
        else:
            return False




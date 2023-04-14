from db.database import *
from typing import Dict
import bcrypt


class Login:
    def __init__(self, email, contrasenia) -> None:
        self.email = email
        self.contrasenia = contrasenia
        self.usuario = self.obtener_usuario()

    def obtener_usuario(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """SELECT udp.`id` id_udp,u.id,u.email, u.contraseña, tu.nombre tipo,udp.`nombre_completo` nombre
                FROM usuarios u
                INNER JOIN tipo_usuario tu on u.id_tipo_usuario = tu.id
                INNER JOIN usuario_datos_personales udp on u.`id_usuario_datos_personales`=udp.`id`
                WHERE u.email=%s"""
        cursor.execute(query, (self.email,))
        return cursor.fetchone()

    def verificar_email(self) -> bool:
        if self.usuario is None:
            return False
        else:
            return True
        
    def verificar_contrasena(self) -> bool:
        if self.usuario is None:
            return True
            
        if bcrypt.checkpw(self.contrasenia.encode('utf-8'), self.usuario['contraseña'].encode('utf-8')):
            return True
        else:
            return False



class ContrasenaUsuarioIncorrecto(Exception):
    ...

class EmailUsuarioIncorrecto(Exception):
    ...

class EmailContraseniaIncorrecta(Exception):
    ...

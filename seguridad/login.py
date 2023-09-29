from db.database import *
from typing import Dict
import bcrypt
from psycopg2 import extras


class Login:
    def __init__(self, email="", contrasenia="") -> None:
        self.email = email
        self.contrasenia = contrasenia
        self.usuario:str = self.obtener_usuario()

    # obtener_informacion
    def obtener_usuario(self) -> Dict:

        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """SELECT udp.id id_udp,u.id,u.email, u.contraseña, tu.nombre tipo, udp.nombre_completo nombre
                FROM usuarios u
                INNER JOIN tipo_usuario tu on u.id_tipo_usuario = tu.id
                INNER JOIN usuario_datos_personales udp on u.id_usuario_datos_personales=udp.id
                WHERE u.email=%s"""
        
        cursor.execute(query, (self.email,))
        return cursor.fetchone()
    
    def informacion_usuario(self,id) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """SELECT udp.id id_udp,tu.nombre tipo, udp.nombre_completo nombre
                FROM usuarios u
                INNER JOIN tipo_usuario tu on u.id_tipo_usuario = tu.id
                INNER JOIN usuario_datos_personales udp on u.id_usuario_datos_personales=udp.id
                WHERE u.id=%s"""
        
        cursor.execute(query, (id,))
        return cursor.fetchone()

    def verificar_usuario(self) -> bool:
        if self.usuario is None:
            return False

        hashed_password = self.usuario['contraseña']
        
        if hashed_password[0:1]=='$':
            hashed_password = hashed_password.encode('utf-8')
        else:
            hashed_password = bytes.fromhex(hashed_password[2:])

        if bcrypt.checkpw(self.contrasenia.encode('utf-8'),hashed_password):
            return True
        else:
            return False

    def verificar_campos_vacios(self) -> bool:
        if len(self.email) == 0 or len(self.contrasenia) == 0:
            return True
        else:
            return False


class CamposVacios(Exception):
    ...


class EmailContraseniaIncorrecta(Exception):
    ...

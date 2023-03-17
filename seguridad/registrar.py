from db.database import *
from typing import Dict
import bcrypt


class Usuario:
    def __init__(self, email: str, contrasenia: str, rol: int, nombre: str, tipo_documento: int, numero_documento: int,celular:int,direccion:str) -> None:
        self.email = email
        self.contrasenia = contrasenia
        self.rol = rol
        self.nombre = nombre
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.celular=celular
        self.direccion=direccion

    def datos_unico(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)

        query = """SELECT email, numero_documento 
            FROM usuarios u
            INNER JOIN usuario_datos_personales dp 
            ON u.`id_usuario_datos_personales`=dp.`id`
            WHERE dp.`numero_documento`=%s or u.email=%s"""
        
        cursor.execute(query, (self.numero_documento, self.email,))
        return cursor.fetchone()
    
    def encriptar_contraseña(self)->str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(self.contrasenia.encode('utf-8'), salt)

    # devuelve true si existe un usuario, es decir no se crea otro usuario, si devuelve false si se crea el usuario
    def existe(self) -> bool:
        dato_unico = self.datos_unico()
        if dato_unico is None:
            return False

        if dato_unico:
            return True
        else:
            return True

    def agregar(self) -> None:

        cursor = db.connection.cursor()

        informacion = (self.tipo_documento, self.nombre,
                       self.numero_documento,self.celular,self.direccion)

        usuario_nuevo = (self.email, self.encriptar_contraseña(),
                         self.rol, self.numero_documento)

        query_informacion = """
                    INSERT INTO usuario_datos_personales (id_documento,nombre_completo,numero_documento,numero_celular,direccion)
                    VALUES (%s,%s,%s,%s,%s)
                """

        query = """INSERT usuarios(email,contraseña,id_tipo_usuario,id_usuario_datos_personales)
                SELECT %s,%s,%s,id
                FROM usuario_datos_personales
                WHERE numero_documento=%s
        """

        cursor.execute(query_informacion, (informacion))
        cursor.execute(query, (usuario_nuevo))
        db.connection.commit()
        cursor.close()
        db.connection.close()

        return 'Usuario agregado'

from db.database import *
from typing import Dict
import bcrypt
<<<<<<< HEAD
from flask import request


class Usuario:
    def __init__(self, email: str, contrasenia: str, rol: int, nombre: str, tipo_documento: int, numero_documento: int,descripcion:str) -> None:
=======


class Usuario:
    def __init__(self, email: str, contrasenia: str, rol: int, nombre: str, tipo_documento: int, numero_documento: int) -> None:
>>>>>>> ajustes_finales
        self.email = email
        self.contrasenia = contrasenia
        self.rol = rol
        self.nombre = nombre
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
<<<<<<< HEAD
        self.descripcion=descripcion
=======
>>>>>>> ajustes_finales

    def datos_unico_documento(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        #revisar
        query = """SELECT u.id
            FROM usuarios u
            INNER JOIN usuario_datos_personales dp 
            ON u.`id_usuario_datos_personales`=dp.`id`
            WHERE dp.`numero_documento`=%s"""
        
        cursor.execute(query, (self.numero_documento,))
        return cursor.fetchone()
    
    def datos_unico_correo(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        #revisar
        query = """SELECT u.id
            FROM usuarios u
            INNER JOIN usuario_datos_personales dp 
            ON u.`id_usuario_datos_personales`=dp.`id`
            WHERE u.email=%s"""
        
        cursor.execute(query, (self.email,))
        return cursor.fetchone()
    
    def encriptar_contraseña(self)->str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(self.contrasenia.encode('utf-8'), salt)

    # devuelve true si existe un usuario, es decir no se crea otro usuario, si devuelve false si se crea el usuario
    def existe_correo (self) -> bool:
        dato_unico = self.datos_unico_correo()
        if dato_unico is None:
            return False
        if dato_unico:
             return True
        else:
            return True
        
    def existe_documento(self) -> bool:
        dato_unico = self.datos_unico_documento()
        if dato_unico is None:
            return False
        if dato_unico:
            return True
        else:
            return True
        
    def existe_(self) -> bool:
        dato_unico_documento = self.datos_unico_documento()
        dato_unico_correo = self.datos_unico_correo()
        if dato_unico_documento is None and dato_unico_correo is None:
            return False
        if dato_unico_documento and dato_unico_correo:
            return True
        else:
            return True

    def agregar(self) -> None:

        cursor = db.connection.cursor()

        informacion = (self.tipo_documento, self.nombre,
<<<<<<< HEAD
                       self.numero_documento,self.descripcion)
=======
                       self.numero_documento)
>>>>>>> ajustes_finales

        usuario_nuevo = (self.email, self.encriptar_contraseña(),
                         self.rol, self.numero_documento)

        query_informacion = """
<<<<<<< HEAD
                    INSERT INTO usuario_datos_personales (id_documento,nombre_completo,numero_documento,descripcion)
                    VALUES (%s,%s,%s,%s)
=======
                    INSERT INTO usuario_datos_personales (id_documento,nombre_completo,numero_documento)
                    VALUES (%s,%s,%s)
>>>>>>> ajustes_finales
                """
        #revisar
        query = """INSERT usuarios(email,contraseña,id_tipo_usuario,id_usuario_datos_personales)
                SELECT %s,%s,%s,id
                FROM usuario_datos_personales
                WHERE numero_documento=%s
        """

        cursor.execute(query_informacion, (informacion))
        cursor.execute(query, (usuario_nuevo))
        db.connection.commit()

        return None
<<<<<<< HEAD
    
    def valor_invalido(self)->bool:
        input_descripcion=request.get_json()['descripcion']
        if input_descripcion != '' and self.rol==3:
            return True
        else:
            return False
=======
>>>>>>> ajustes_finales



class CorreoExistenteException(Exception):
    """
    Excepción personalizada para indicar que el correo electrónico ya existe.
    """
    pass


class DocumentoExistenteException(Exception):
    """
    Excepción personalizada para indicar que el número de documento ya existe.
    """
    pass


class ExistenteException(Exception):
    """
    Excepción personalizada para indicar que el número de documento y el correo electrónico ya existe.
    """
    pass
<<<<<<< HEAD

class DatosInvalidoException(Exception):
    """
    Excepción personalizada para indicar que el valor ingresado no es pedido.
    """
    pass


=======
>>>>>>> ajustes_finales

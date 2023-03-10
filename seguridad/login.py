from db.database import *
from typing import Dict


class Usuario:
    def __init__(self) -> None:
        pass


class Login:
    def __init__(self, email, contrasenia) -> None:
        self.email = email
        self.contrasenia = contrasenia
        self.usuario = self.obtener_usuario()

    def datos_unico(self, numero_documento, email) -> Dict:
        cursor = db.connection.cursor(dictionary=True)

        query = """SELECT email, numero_documento 
            FROM usuarios u
            INNER JOIN usuario_datos_personales dp 
            ON u.`id`=dp.`id_usuario`
            WHERE dp.`numero_documento`=%s or u.email=%s"""
        cursor.execute(query, (numero_documento, email,))
        return cursor.fetchone()

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


class RegistroUsuario(Login):

    def __init__(self, email: str, contrasenia: str, rol: int, nombre: str, tipo_documento: int, numero_documento: int) -> None:
        self.email = email
        self.contrasenia = contrasenia
        self.rol = rol
        self.nombre = nombre
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento

        super().__init__(email, contrasenia)

    # devuelve true si existe un usuario, es decir no se crea otro usuario, si devuelve false si se crea el usuario
    def existe(self) -> bool:
        dato_unico = self.datos_unico(
            numero_documento=self.numero_documento, email=self.email)
        if dato_unico is None:
            return False

        if dato_unico:
            return True
        else:
            return True

    def agregar(self) -> None:
        cursor = db.connection.cursor()
        usuario_nuevo = (self.email, self.contrasenia, self.rol)
        informacion = (self.tipo_documento, self.nombre,
                       self.numero_documento, self.email)
        query = "INSERT INTO usuarios (email,contraseña,id_tipo_usuario) VALUES (%s,%s,%s)"
        query_informacion = """
                    INSERT usuario_datos_personales (id_usuario,id_documento,nombre_completo,numero_documento)
                    SELECT id,%s,%s,%s
                    FROM usuarios
                    WHERE email=%s
                """
        cursor.execute(query, (usuario_nuevo))
        cursor.execute(query_informacion, (informacion))
        db.connection.commit()
        cursor.close()
        db.connection.close()

        return None

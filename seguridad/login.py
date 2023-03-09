import json
from db.database import *


class Login:
    def __init__(self, email, contrasenia) -> None:
        self.email = email
        self.contrasenia = contrasenia
        self.cuenta = self.cuentas()

    def cuentas(self) -> list:
        cursor = db.connection.cursor()
        query = """SELECT u.email, u.contraseña, tu.nombre tipo,u.nombre,u.numero_documento
            FROM usuarios u
            INNER JOIN tipo_usuario tu on u.id_tipo_usuario = tu.id"""
        cursor.execute(query)
        return cursor.fetchall()

    def usuario(self) -> bool:
        for user in self.cuenta:
            if (user[0] == self.email and user[1] == self.contrasenia):
                return True
        return False

    def tipo_usuario(self) -> str:
        for user in self.cuenta:
            if (user[0] == self.email and user[1] == self.contrasenia):
                return user[2]
        return ""

    def nombre_usuario(self) -> str:
        for user in self.cuenta:
            if (user[0] == self.email and user[1] == self.contrasenia):
                nombre: str = user[3]
                return nombre.upper()
        return ""


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
    def existe(self, email, numero_documento) -> bool:
        for usuario in self.cuenta:
            if usuario[4]==numero_documento or usuario[0] == email:
                return True
        return False

    def agregar(self) -> None:
        cursor = db.connection.cursor()

        usuario_nuevo = (self.nombre, self.email, self.contrasenia,
                         self.numero_documento, self.tipo_documento, self.rol)
        query = "INSERT INTO usuarios (nombre,email,contraseña,numero_documento,id_documento,id_tipo_usuario) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (usuario_nuevo))
        db.connection.commit()
        cursor.close()
        db.connection.close()

        return None

import json
from db.database import *


class Login:
    def __init__(self, usuario, contrasenia) -> None:
        self.email = usuario
        self.contrasenia = contrasenia
        self.cuenta = self.cuentas()

    def cuentas(self) -> list:
        cursor = db.connection.cursor()
        query = """SELECT u.email, u.contraseña, tu.nombre tipo,u.nombre
            FROM usuarios u
            INNER JOIN tipo_usuario tu on u.id_tipo_usuario = tu.id"""
        cursor.execute(query)
        return cursor.fetchall()

    def usuario(self) -> bool:
        for user in self.cuenta:
            if (user[0] == self.email and user[1] == self.contrasenia):
                return True
        return False

    def tipo_usuario(self):
        for user in self.cuenta:
            if (user[0] == self.email and user[1] == self.contrasenia):
                return user[2]
        return 0

    def nombre_usuario(self) -> str:
        for user in self.cuenta:
            if (user[0] == self.email and user[1] == self.contrasenia):
                nombre:str= user[3]
                return nombre.upper()
        return ""


class RegistroUsuario(Login):

    def __init__(self, rol, usuario, contrasenia) -> None:
        self.rol = rol
        self.user = usuario
        self.contrasenia = contrasenia
        super().__init__(usuario, contrasenia)

    # devuelve true si existe un usuario, es decir no se crea otro usuario, si devuelve false si se crea el usuario
    def existe(self, rol, usuario, contrasenia):
        for user in self.cuenta:
            if (user['rol'] == rol and user['usuario'] == usuario and user['contrasenia'] == contrasenia):
                return True
        return False

    def agregar(self):
        nuevo_usuario = {"rol": self.rol,
                         "usuario": self.user, "contrasenia": self.contrasenia}
        self.cuenta.append(nuevo_usuario)
        datos_actualizados = json.dumps(self.cuenta)
        return datos_actualizados

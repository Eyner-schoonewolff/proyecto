from db.database import *

class Usuario:
    def __init__(self) -> None:
        pass

class Login:
    def __init__(self, email, contrasenia) -> None:
        self.email = email
        self.contrasenia = contrasenia
        self.cuenta = self.cuentas()
        self.datos_unicos = self.datos_unico()

    def datos_unico(self) -> list:
        cursor = db.connection.cursor()
        query = """SELECT email, numero_documento 
            FROM usuarios u
            INNER JOIN usuario_datos_personales dp 
            ON u.`id`=dp.`id_usuario`"""
        cursor.execute(query)
        return cursor.fetchall()

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
        for usuario in self.datos_unicos:
            if usuario[0] == email or usuario[1] == numero_documento:
                return True
        return False

    def agregar(self) -> None:
        cursor = db.connection.cursor()
        usuario_nuevo = (self.nombre, self.email, self.contrasenia, self.rol)
        informacion = (self.tipo_documento, self.numero_documento, self.email)
        query = "INSERT INTO usuarios (nombre,email,contraseña,id_tipo_usuario) VALUES (%s,%s,%s,%s)"
        query_informacion = """
                    INSERT usuario_datos_personales (id_usuario,id_documento,numero_documento)
                    SELECT id,%s,%s
                    FROM usuarios
                    WHERE email=%s
                """
        cursor.execute(query, (usuario_nuevo))
        cursor.execute(query_informacion, (informacion))
        db.connection.commit()
        cursor.close()
        db.connection.close()

        return None

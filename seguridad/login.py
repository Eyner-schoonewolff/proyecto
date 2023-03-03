import json

class Login:
    def __init__(self, usuario, contrasenia) -> None:
        self.email = usuario
        self.contrasenia = contrasenia
        self.cuenta = self.cuentas()

    def cuentas(self)->list:
        with open("informacion/cuentas.json", "r") as j:
            self.cuenta = json.load(j)
            return self.cuenta

    def usuario(self) -> bool:
        email = self.email
        contrasenia = self.contrasenia

        for user in self.cuenta:
            if (user['usuario'] == email and user['contrasenia'] == contrasenia):
                return True
        return False


class RegistroUsuario(Login):

    def __init__(self, rol, usuario, contrasenia) -> None:
        self.rol = rol
        self.user = usuario
        self.contrasenia = contrasenia
        super().__init__(usuario,contrasenia)

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

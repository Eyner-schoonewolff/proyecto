import json


class Login:
    def __init__(self, usuario, contraseña) -> None:
        self.email=usuario
        self.contraseña=contraseña
        self.cuenta=self.cuentas()

    def cuentas(self):
        with open("informacion/cuentas.json", "r") as j:
            self.cuenta = json.load(j)
            return self.cuenta

    @property
    def cuentas(self):
        return self.__cuenta
    
    @cuentas.setter
    def cuentas(self,cuentas):
        self.__cuenta=cuentas

    def usuario(self) -> bool:
        email = self.email
        contraseña = self.contraseña

        for user in self.cuenta:
            if (user['usuario'] == email and user['contraseña'] == contraseña):
                return True
        return False


class Registro(Login):
    def __init__(self) -> None:
        super().__init__()

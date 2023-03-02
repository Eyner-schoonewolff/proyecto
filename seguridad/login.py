from flask import request
import json

class Login(object):
    def __init__(self) -> None:
         with open("informacion/cuentas.json", "r") as j:
            self.cuenta = json.load(j)

    def __request_usuario(self):
        return request.get_json()

    def usuario(self) -> bool:
        email = self.__request_usuario()['email']
        contraseña = self.__request_usuario()['contraseña']
       
        for user in self.cuenta:
            if(user['usuario'] == email and user['contraseña'] == contraseña):
                return True    
        return False

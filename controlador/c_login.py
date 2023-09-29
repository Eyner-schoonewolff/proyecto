from seguridad.login import *
from seguridad.datos_usuario import DatosUsuario
from decorador.decoradores import *
from flask import redirect, url_for, request, jsonify
from flask_jwt_extended import create_access_token
import datetime

class Login_controlador():
    def validar_campos_vacios_usuario(self,id,tipo_usuario)->str:

        datos_usuario = DatosUsuario(id_usuario=id,tipo_usuario=tipo_usuario)

        if datos_usuario.validar_campos_vacios():
            return '/templates/actualizar.html'
        else:
            return '/templates/home.html'

    def auth(self):
        json = request.get_json()
        email = json['email']
        contrasenia = json['contrasenia']

        login = Login(email = email, contrasenia = contrasenia)

        try:
            if login.verificar_campos_vacios():
                raise CamposVacios(
                    "Por favor verifique que los campos no estén vacíos")
            elif not login.verificar_usuario():
                raise EmailContraseniaIncorrecta(
                    "El email y/o contraseña ingresada es incorrecto")
            else:

                usuario = {
                    'id': login.usuario['id'],
                    'id_udp': login.usuario['id_udp'],
                    'email': login.usuario['email'],
                    'username': login.usuario["nombre"].upper(),
                    'tipo_usuario': login.usuario["tipo"],
                    'exp':datetime.datetime.utcnow()+ datetime.timedelta(minutes=30),
                    'exp_token_seg':str(datetime.timedelta(minutes=30))
                }

                access_token = create_access_token(identity=usuario)

                home = self.validar_campos_vacios_usuario(login.usuario['id'],login.usuario["tipo"])

                return jsonify({
                    "login": True,
                    "nombre":login.usuario["nombre"].upper(),
                    "id":login.usuario['id'],
                    "token": access_token,
                    "exp":usuario['exp'],
                    "exp_token_seg":usuario['exp_token_seg'],
                    "home": home,
                })

        except CamposVacios as mensaje:
            return {"login": False, "home": "/templates/index.html", "excepcion": str(mensaje)}
        except EmailContraseniaIncorrecta as mensaje:
            return {"login": False, "home": "/templates/index.html", "excepcion": str(mensaje)}

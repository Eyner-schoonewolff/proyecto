from seguridad.login import *
from seguridad.datos_usuario import DatosUsuario
from decorador.decoradores import *
from flask import redirect, url_for, request, jsonify
from flask_jwt_extended import create_access_token
import datetime


class Login_controlador():
    def validar_campos_vacios(self):
        datos_usuario = DatosUsuario()
        if datos_usuario.validar_campos_vacios():
            return redirect(url_for('datos_personales.actualizar'))
        else:
            return redirect(url_for('menus.home'))

    def auth(self):
        json = request.get_json()
        email = json['email']
        contrasenia = json['contrasenia']

        login = Login(email=email, contrasenia=contrasenia)

        try:
            if login.verificar_campos_vacios():
                raise CamposVacios(
                    "Por favor verifique que los campos no estén vacíos")
            elif not login.verificar_usuario():
                raise EmailContraseniaIncorrecta(
                    "El email y/o contraseña ingresada es incorrecto")
            else:
                identificadores = {
                    'id': login.usuario['id'],
                    'id_udp': login.usuario['id_udp'],
                    'email': login.usuario['email'],
                    'username': login.usuario["nombre"].upper(),
                    'tipo_usuario': login.usuario["tipo"],
                    'exp':datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
                }

                access_token = create_access_token(identity=identificadores)


                return jsonify({
                    "login": True,
                    "token": access_token,
                    "home": "/templates/home.html",
                })

        except CamposVacios as mensaje:
            return {"login": False, "home": "/templates/index.html", "excepcion": str(mensaje)}
        except EmailContraseniaIncorrecta as mensaje:
            return {"login": False, "home": "/templates/index.html", "excepcion": str(mensaje)}

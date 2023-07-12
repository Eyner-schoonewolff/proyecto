from seguridad.login import *
from seguridad.datos_usuario import DatosUsuario
from decorador.decoradores import *
from flask import redirect, url_for, session, request, jsonify


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
                    "Por favor verifique que los campos no esten vacios")
            elif not login.verificar_usuario():
                raise EmailContraseniaIncorrecta(
                    "El email y/o contraseña ingresada es incorrecto")
            else:
                # Generar token
                session['login'] = True
                session['id'] = login.usuario['id']
                session['id_udp'] = login.usuario['id_udp']
                session['email'] = login.usuario['email']
                session['username'] = login.usuario["nombre"].upper()
                session['tipo_usuario'] = login.usuario["tipo"]

                return jsonify({'id_usuario': login.usuario['id'], 
                                'id_usuario_datos_personales':login.usuario['id_udp'],
                                "login": True, 
                                "home": "/",
                                'email': login.usuario['email'], 
                                'tipo':login.usuario["tipo"],
                                'nombre':login.usuario["nombre"].upper()
                                })

        except CamposVacios as mensaje:
            session['login'] = False
            return {"login": False, "home": "/", "excepcion": str(mensaje)}
        except EmailContraseniaIncorrecta as mensaje:
            session['login'] = False
            return {"login": False, "home": "/", "excepcion": str(mensaje)}

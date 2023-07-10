from seguridad.login import *
from seguridad.datos_usuario import DatosUsuario
from decorador.decoradores import *


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
                session['login'] = True
                session['id'] = login.usuario['id']
                session['id_udp'] = login.usuario['id_udp']
                session['email'] = login.usuario['email']
                session['username'] = login.usuario["nombre"].upper()
                session['tipo_usuario'] = login.usuario["tipo"]
                return {"login": True, "home": "/"}

        except CamposVacios as mensaje:
            session['login'] = False
            return {"login": False, "home": "/", "excepcion": str(mensaje)}
        except EmailContraseniaIncorrecta as mensaje:
            session['login'] = False
            return {"login": False, "home": "/", "excepcion": str(mensaje)}
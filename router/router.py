from flask import Blueprint, render_template, redirect, url_for, request, session
from seguridad.login import *
from flask_login import logout_user, LoginManager
from seguridad.datos_usuario import DatosUsuario
from decorador.decoradores import  *

login = Blueprint('login', __name__, static_url_path='/static',
                  template_folder="templates")

login_manager = LoginManager()

def notFound(error):
    return render_template('noEncontrada.html'),404

@login.route("/inicio",endpoint='inicio', methods=["GET"])
@login_ruta_acceso
def inicio():
        return render_template("/index.html")

@login.route("/",endpoint='/', methods=["GET"])
@login_required_home
def index():
    datos_usuario=DatosUsuario()

    if datos_usuario.validar_campos_vacios():
        return redirect(url_for('datos_personales.actualizar'))
    else:
        return redirect(url_for('menus.home'))


@login.route("/auth", methods=["POST","GET"])
@proteccion_ruta
def auth():
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


@login.route('/logout')
@login_manager.user_loader
def logout():
    logout_user()
    session['login'] = False
    return redirect(url_for('login./'))

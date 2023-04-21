from flask import Blueprint, render_template, redirect, url_for, request, session
from seguridad.login import *
from flask_login import logout_user, LoginManager
<<<<<<< HEAD
from seguridad.datos_usuario import DatosUsuario
=======
>>>>>>> ajustes_finales

login = Blueprint('login', __name__, static_url_path='/static',
                  template_folder="templates")

login_manager = LoginManager()


@login.route("/", methods=["GET"])
def index():
    logueado = session.get('login')
    if not logueado:
        return render_template("/index.html")
<<<<<<< HEAD
    
    datos_usuario=DatosUsuario()

    if datos_usuario.validar_campos_vacios():
        return redirect(url_for('datos_personales.actualizar'))
=======
>>>>>>> ajustes_finales
    else:
        return redirect(url_for('menus.home'))


@login.route("/auth", methods=["POST"])
def auth():
    json = request.get_json()
    email = json['email']
    contrasenia = json['contrasenia']

    login = Login(email=email, contrasenia=contrasenia)

    try:
        if not (login.verificar_contrasena() or login.verificar_email()):
            raise EmailContraseniaIncorrecta(
                "Email y contraseña incorrecta por favor validar")
        elif not login.verificar_email():
            raise EmailUsuarioIncorrecto(
                "El email ingresada es incorrecto")

        elif not login.verificar_contrasena():
            raise ContrasenaUsuarioIncorrecto(
                "La contraseña ingresada es incorrecta")
        else:
            session['login'] = True
            session['id'] = login.usuario['id']
            session['id_udp'] = login.usuario['id_udp']
            session['email'] = login.usuario['email']
            session['username'] = login.usuario["nombre"].upper()
            session['tipo_usuario'] = login.usuario["tipo"]
<<<<<<< HEAD
            return {"login": True, "home": "/"}
=======
            return {"login": True, "home": "/actualizar"}
>>>>>>> ajustes_finales

    except EmailContraseniaIncorrecta as mensaje:
        session['login'] = False
        return {"login": False, "home": "/", "excepcion": str(mensaje)}
    except EmailUsuarioIncorrecto as mensaje:
        session['login'] = False
        return {"login": False, "home": "/", "excepcion": str(mensaje)}
    except ContrasenaUsuarioIncorrecto as mensaje:
        session['login'] = False
        return {"login": False, "home": "/", "excepcion": str(mensaje)}


@login.route('/logout')
@login_manager.user_loader
def logout():
    logout_user()
    session['login'] = False
    return redirect(url_for('login.index'))

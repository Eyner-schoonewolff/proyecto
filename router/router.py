from flask import Blueprint, render_template, redirect, url_for, request, session
from seguridad.login import Login
from flask_login import logout_user, LoginManager

login = Blueprint('login', __name__, static_url_path='/static',
                  template_folder="templates")

login_manager = LoginManager()


@login.route("/", methods=["GET"])
def index():
    logueado = session.get('login')
    if not logueado:
        return render_template("/index.html")
    else:
        return redirect(url_for('datos_personales.home'))


@login.route("/auth", methods=["POST"])
def auth():
    json = request.get_json()
    email = json['email']
    contrasenia = json['contrasenia']

    login = Login(email=email, contrasenia=contrasenia)

    if login.verificar():
        session['login'] = True
        session['id'] = login.usuario['id']
        session['id_udp'] = login.usuario['id_udp']
        session['email'] = login.usuario['email']
        session['username'] = login.usuario["nombre"].upper()
        session['tipo_usuario'] = login.usuario["tipo"]
        return {"login": True, "home": "/home"}

    session['login'] = False
    return {"login": False, "home": "/"}


@login.route('/logout')
@login_manager.user_loader
def logout():
    logout_user()
    session['login'] = False
    return redirect(url_for('login.index'))

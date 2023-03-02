from flask import Blueprint, render_template, redirect, url_for, request, session
from seguridad.login import Login
from flask_login import logout_user, LoginManager

login = Blueprint('login', __name__, static_url_path='/static',
                  template_folder="templates")

login_manager = LoginManager()

verificacion = Login()


@login.route("/", methods=["GET"])
def index():
    return render_template("/index.html")


@login.route("/home")
def home():
    username = session.get('username')
    logueado = session.get('login')
    print(logueado)
    if logueado:
        session['login'] = True
        return render_template("home.html", nombre=username)
    else:
        session['login'] = False
        return redirect(url_for('login.index'))


@login.route("/auth", methods=["GET", "POST"])
def auth():
    usuario = request.get_json()
    email = usuario['email']

    if verificacion.usuario():
        session['login'] = True
        session['username'] = email
        return {"login": True, "home": "/home"}

    session['login'] = False
    return {"login": False, "home": "/"}


@login.route('/logout')
@login_manager.user_loader
def logout():
    logout_user()
    session['login'] = False
    return redirect(url_for('login.index'))

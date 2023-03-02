from flask import Blueprint, render_template, redirect, url_for, request, session
from seguridad.login import Login
from flask_login import logout_user, LoginManager

login = Blueprint('login', __name__, static_url_path='/static',
                  template_folder="templates")

login_manager = LoginManager()


@login.route("/registrar")
def registro():
    logueado=session.get('login')
    if not logueado:
        return render_template("registrar.html")    
    else:
        return redirect(url_for('login.home'))


@login.route("/", methods=["GET"])
def index():
    logueado = session.get('login')
    if not logueado:
        return render_template("/index.html")
    else:
        return redirect(url_for('login.home'))


@login.route("/home")
def home():
    username = session.get('username')
    logueado = session.get('login')
    if logueado:
        return render_template("home.html", nombre=username)
    else:
        return redirect(url_for('login.index')) 


@login.route("/auth", methods=["GET", "POST"])
def auth():
    usuario = request.get_json()
    email = usuario['email']
    contraseña = usuario['contraseña']

    verificacion = Login(usuario=email, contraseña=contraseña)

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




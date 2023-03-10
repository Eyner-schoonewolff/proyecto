from flask import Blueprint, render_template, redirect, url_for, request, session
from seguridad.login import Login, RegistroUsuario
from flask_login import logout_user, LoginManager

login = Blueprint('login', __name__, static_url_path='/static',
                  template_folder="templates")

login_manager = LoginManager()


@login.route("/registrar")
def registro():
    logueado = session.get('login')
    if not logueado:
        return render_template("registrar.html")
    else:
        return redirect(url_for('login.home'))


@login.route("/auth_register", methods=["POST"])
def auth_register():
    usuario_nuevo = request.get_json()
    email =str(usuario_nuevo['email'])
    contrasenia = usuario_nuevo['contrasenia']
    rol = int(usuario_nuevo['rol'])
    nombre = usuario_nuevo['nombre']
    tipo_documento = int(usuario_nuevo['tipo_documento'])
    numero_documento = int(usuario_nuevo['numero_documento'])

    registro_usuario = RegistroUsuario(email=email, contrasenia=contrasenia, rol=rol,
                                       nombre=nombre, tipo_documento=tipo_documento, numero_documento=numero_documento)

    if registro_usuario.existe():
        return {"registro": False, "home": "/registrar"}
    else:
        registro_usuario.agregar()
        return {"registro": True, "home": "/"}


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
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login')
    if logueado:
        session['login'] = True
        return render_template("home.html", nombre=username, tipo=tipo_usuario)
    else:
        session['login'] = False
        return redirect(url_for('login.index'))


@login.route("/auth", methods=["POST"])
def auth():
    json = request.get_json()
    email = json['email']
    contrasenia = json['contrasenia']

    login = Login(email=email, contrasenia=contrasenia)

    if login.verificar():
        session['login'] = True
        session['username'] = login.usuario["nombre"]
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

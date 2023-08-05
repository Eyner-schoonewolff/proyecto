from flask import Blueprint, render_template, redirect, url_for, jsonify, session,send_from_directory
from seguridad.login import *
from flask_login import logout_user, LoginManager
from decorador.decoradores import  *
from controlador.c_login import Login_controlador
from flask_cors import cross_origin

login = Blueprint('login', __name__, static_url_path='/static',
                  template_folder="templates")

login_manager = LoginManager()

# def notFound(error):
#     return render_template('noEncontrada.html'),404

@login.route("/inicio",endpoint='inicio', methods=["GET"])
@cross_origin()
# @login_ruta_acceso
def inicio():
        return jsonify({'template':'index.html'})

@login.route("/",endpoint='/', methods=["GET"])
@cross_origin()
# @login_required_home
def index():
    c_login=Login_controlador()
    return c_login.validar_campos_vacios()

@login.route("/auth", methods=["POST","GET"])
@cross_origin()
# @proteccion_ruta
def auth():
    c_login=Login_controlador()
    return c_login.auth()

@login.route('/logout')
@cross_origin()
@login_manager.user_loader
def logout():
    logout_user()
    #eliminar token
    return redirect(url_for('inicio'))

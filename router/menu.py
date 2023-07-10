from flask import Blueprint
from decorador.decoradores import *
from controlador.c_menu import *


menus = Blueprint('menus', __name__, static_url_path='/static',
                  template_folder="templates")


@menus.route('/home', endpoint='home')
@login_required_home
def home():
    c_menu = Menu_controlador()
    return c_menu.home()

@menus.route('/perfiles', endpoint='perfiles')
@login_required_home
def perfiles():
    c_menu = Menu_controlador()
    return c_menu.perfiles()

@menus.route('/perfiles/<id>', endpoint="perfiles_id", methods=['POST', 'GET'])
@proteccion_ruta
def perfiles_cliente(id):
    c_menu = Menu_controlador()
    return c_menu.perfiles_cliente(id)

@menus.route('/perfiles_contra', endpoint='consultar_contratista')
@login_required_home
@proteccion_ruta_admin
def perfiles_contra():
    c_menu = Menu_controlador()
    return c_menu.perfiles_contratista()


@menus.route("/solicitar", endpoint='solicitar', methods=['GET', 'POST'])
@login_required_home
@proteccion_ruta_admin
def solicitar_contratista():
    c_menu = Menu_controlador()
    return c_menu.solicitar_contratista()

@menus.route("/consultar", endpoint='consultar')
@login_required_home
@proteccion_ruta_admin
def consultar():
    c_menu = Menu_controlador()
    return c_menu.consultar()

@menus.route("/consultar/admin", endpoint='consultar_admin')
@login_required_home
@proteccion_acceso_usuarios
def consultar_admin():
    c_menu = Menu_controlador()
    return c_menu.consultar_admin()


@menus.route("/actualizar_estado/<id>", methods=['POST'])
def actualizar_estado(id):
    c_menu = Menu_controlador()
    return c_menu.consultar_estado(id)

@menus.route("/evidencia/<id>", endpoint='evidencias', methods=['GET'])
@login_required_home
@proteccion_ruta_admin
def evidencia_solicitud(id):
    c_menu = Menu_controlador()
    return c_menu.evidencia(id)

@menus.route("/contacto", endpoint='contacto')
@login_required_home
@proteccion_ruta_admin
def contacto():
    c_menu = Menu_controlador()
    return c_menu.contacto()

@menus.route("/calendario", endpoint='calendario')
@login_required_home
@proteccion_ruta_admin
def calendario():
    c_menu = Menu_controlador()
    return c_menu.calendario()

@menus.route("/calificar", endpoint='calificar')
@login_required_home
@proteccion_ruta_admin
def calificar():
    c_menu = Menu_controlador()
    return c_menu.calificar()


@menus.route("/guardar-calificacion", methods=['POST'])
def guardar_calificacion():
    c_menu = Menu_controlador()
    return c_menu.guardar_calificacion()


@menus.route("/enviar_correos", methods=['POST'])
def enviar_correos():
    c_menu = Menu_controlador()
    return c_menu.enviar_correos()

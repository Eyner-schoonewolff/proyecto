from flask import Blueprint, render_template
from seguridad.datos_usuario import DatosUsuario, DatoUnicoEmail, CorreoInvalido
from seguridad.Model_solicitar_servicio import *
from decorador.decoradores import *
from controlador.c_datos_personales import *
from flask_cors import cross_origin


datos_personales = Blueprint('datos_personales', __name__, static_url_path='/static',
                             template_folder="templates")


# def notFound(error):
#     return render_template('noEncontrada.html'), 405


@datos_personales.route("/actualizar", endpoint='actualizar')
@cross_origin()
@jwt_required()
# @login_required_home
def actualizar():
    c_datos_personales = Datos_personales_controlador()
    return c_datos_personales.c_actualizar_ocupaciones()


@datos_personales.route("/actualizar/admin", endpoint='actualizar/admin', methods=['GET', 'POST'])
@cross_origin()
@jwt_required()
# @login_required_home
# @proteccion_acceso_usuarios
def actualizar_admin():
    c_datos_personales = Datos_personales_controlador()
    return c_datos_personales.actualizar_admin()


@datos_personales.route("/actualizar/email_usuario", endpoint='actualizar/email_usuario', methods=['POST', 'GET'])
@cross_origin()
@jwt_required()
# @proteccion_ruta
# @proteccion_acceso_usuarios
def actualizar_email_usuario():
    c_datos_personales = Datos_personales_controlador()
    return c_datos_personales.actualizar_email()


@datos_personales.route('/auth/actualizar', endpoint='auth/actualizar', methods=['POST', 'GET'])
@cross_origin()
@jwt_required()
# @proteccion_ruta
def auth():
    c_datos_personales = Datos_personales_controlador()
    return c_datos_personales.actualizar_informacion()


@datos_personales.route('/ocupaciones_contratista', endpoint='ocupaciones_contratista', methods=['GET'])
@cross_origin()
@jwt_required()
# @proteccion_ruta_admin
def ocup():
    c_datos_personales = Datos_personales_controlador()
    return c_datos_personales.ocupaciones_contratista()


@datos_personales.route('/agregar_ocupaciones', methods=['POST'])
@cross_origin()
@jwt_required()
def agregar():
    c_datos_personales = Datos_personales_controlador()
    return c_datos_personales.agregar_ocupacion()


@datos_personales.route('/contratistas', endpoint='contratistas', methods=['GET'])
@cross_origin()
@jwt_required()
# @proteccion_ruta_admin
def contra():
    c_datos_personales = Datos_personales_controlador()
    return c_datos_personales.informacion_contratista()


@datos_personales.route('/eventos', endpoint='eventos', methods=['GET'])
@cross_origin()
@jwt_required()
# @proteccion_ruta_admin
def event():
    c_datos_personales = Datos_personales_controlador()
    return c_datos_personales.eventos()


@datos_personales.route('/datosestadisticas', endpoint='datosestadisticas', methods=['GET'])
@cross_origin()
@jwt_required()
# @proteccion_ruta_admin
def datoses():
    c_datos_personales = Datos_personales_controlador()
    return c_datos_personales.datosestadistica()


@datos_personales.route('/datosestadisticaslinea', endpoint='datosestadisticaslinea', methods=['GET'])
@cross_origin()
@jwt_required()
# @proteccion_ruta_admin
def datosline():
    c_datos_personales = Datos_personales_controlador()
    return c_datos_personales.datosestadisticaslinea()


@datos_personales.route('/datosestadisticastorta', endpoint='datosestadisticastorta', methods=['GET'])
@cross_origin()
@jwt_required()
# @proteccion_ruta_admin
def datostor():
    c_datos_personales = Datos_personales_controlador()
    return c_datos_personales.datosestadisticastorta()


@datos_personales.route("/header_usuarios", endpoint='header_usuarios')
@cross_origin()
@jwt_required()
# @login_required_home
def header():
    c_datos_personales = Datos_personales_controlador()
    return c_datos_personales.header_usuarios()


@datos_personales.route('/ocupaciones_', endpoint='ocupaciones_', methods=['GET'])
@cross_origin()
@jwt_required()
# @proteccion_ruta_admin
def ocup():
    c_datos_personales = Datos_personales_controlador()
    return c_datos_personales.ocupaciones_()

from flask import Blueprint,render_template,jsonify
from decorador.decoradores import *
from controlador.c_registrar import *
from flask_cors import cross_origin

registrar = Blueprint('registrar', __name__, static_url_path='/static',
                      template_folder="templates")

@registrar.errorhandler(400)
def handle_unsupported_media_type_error(e):
    response = jsonify({'error': 'No se enviaron datos en el cuerpo de la solicitud'})
    response.status_code = 400
    return response

@registrar.route("/registrar")
# @login_required_login
@cross_origin()
def registro():
    return render_template('registrar.html')


@registrar.route("/auth_registro", methods=["POST", "GET"])
@cross_origin()
# @proteccion_ruta
def auth():
    registro=Registrar_controlador()
    return registro.c_agregar_usuario()

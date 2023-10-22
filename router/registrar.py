from flask import Blueprint,jsonify
from decorador.decoradores import *
from controlador.c_registrar import *
from flask_cors import cross_origin
from modelo_validacion.registrar_usuario import UsuarioModelo

registrar = Blueprint('registrar', __name__, static_url_path='/static',
                      template_folder="templates")

@registrar.errorhandler(400)
def handle_unsupported_media_type_error(e):
    response = jsonify({'error': 'No se enviaron datos en el cuerpo de la solicitud'})
    response.status_code = 400
    return response


@registrar.route("/auth_registro", methods=["POST"])  # /usuario [POST]
@cross_origin()
# @proteccion_ruta
def registar_usuario(): #registar_usuario
    usuario_controlador = UsuarioControlador()
    try:
        usuario_nuevo = request.get_json()
        datos_validos = UsuarioModelo(**usuario_nuevo)
        return usuario_controlador.agregar_usuario(datos_validos)
    
    except ValidationError as e:
            errores = e.errors()
            obtener_mensaje_errores = usuario_controlador.mensaje_error(errores)
            return {"registro": False, "mensaje": obtener_mensaje_errores}
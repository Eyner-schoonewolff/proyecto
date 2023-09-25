from flask import Blueprint
from decorador.decoradores import *
from flask_cors import cross_origin
from controlador.c_notificaciones import Notificacion_controlador

notificacion = Blueprint('notificacion', __name__, static_url_path='/static',
                  template_folder="templates")


@notificacion.route('/notificacion', endpoint = 'notificacion', methods=['GET'])
@cross_origin()
@jwt_required()
def notificaciones():
   controlador = Notificacion_controlador()
   return controlador.obtener_notificaciones()


@notificacion.route('/leer_notificacion',endpoint ='notificaion_activar', methods=['POST'])
@cross_origin()
@jwt_required()
def notificacion_leida():
   id = request.get_json()
   controlador = Notificacion_controlador()
   return controlador.leer_notificacion(id)

@notificacion.route('/eliminar_notificacion',endpoint ='eliminar_notificacion', methods=['POST'])
@cross_origin()
@jwt_required()
def notificacion_eliminada():
   id = request.get_json()
   controlador = Notificacion_controlador()
   return controlador.eliminar_notificacion(id)


@notificacion.route('/cantidad_notificacion/<id>', endpoint = 'cantidad_notificacion', methods=['GET'])
@cross_origin()
@jwt_required()
def numero_de_notificaciones(id):
    controlador = Notificacion_controlador()
    return controlador.obtener_numero_de_notificacion(id)
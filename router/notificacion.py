from flask import Blueprint
from decorador.decoradores import *
from flask_cors import cross_origin
from controlador.c_notificaciones import Notificacion_controlador

notifiacion = Blueprint('notificacion', __name__, static_url_path='/static',
                  template_folder="templates")


@notifiacion.route('/notificacion', endpoint = 'notificacion', methods=['GET'])
@cross_origin()
@jwt_required()
def notificacion():
   controlador = Notificacion_controlador()
   return controlador.obtener_notificaciones()


@notifiacion.route('/leer_notificacion',endpoint ='notificaion_activar', methods=['POST'])
@cross_origin()
@jwt_required()
def notificacion_leida():
   id = request.get_json()
   controlador = Notificacion_controlador()
   return controlador.leer_notificacion(id)

@notifiacion.route('/eliminar_notificacion',endpoint ='eliminar_notificacion', methods=['POST'])
@cross_origin()
@jwt_required()
def notificacion_eliminada():
   id = request.get_json()
   controlador = Notificacion_controlador()
   return controlador.eliminar_notificacion(id)
from flask import Blueprint
from decorador.decoradores import *
from flask_cors import cross_origin
from controlador.c_notificaciones import Notificacion_controlador

notifiacion = Blueprint('notificacion', __name__, static_url_path='/static',
                  template_folder="templates")


@notifiacion.route('/notificacion', endpoint='notificacion', methods=['GET'])
@cross_origin()
@jwt_required()
def barra_notificacion():
   notificaciones=Notificacion_controlador()
   return notificaciones.c_informacion()
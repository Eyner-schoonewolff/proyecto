from flask import request, session, render_template, jsonify
from decorador.decoradores import *
import json
from flask_jwt_extended import get_jwt_identity, jwt_required
from seguridad.notificacion import *

class Notificacion_controlador():
    def __init__(self) -> None:
        pass


    def c_informacion(self):
        identificadores=get_jwt_identity()
        id=identificadores.get('id')
        tipo = identificadores.get('tipo_usuario')

        notificacion=Noticacion()

        if tipo=='Contratista':
            datos=notificacion.informacion_contratista(id)
            return jsonify({'informacion':datos})
        else:
            ...

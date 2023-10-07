from flask import jsonify
from decorador.decoradores import *
from flask_jwt_extended import get_jwt_identity, jwt_required
from seguridad.notificacion import *

class Notificacion_controlador():
    def __init__(self) -> None:
        pass


    def obtener_notificaciones(self):
        usuario : dict = get_jwt_identity()
        id_usuario = usuario.get('id')

        notificacion = Noticacion()

        datos = notificacion.obtener_notificaciones_contratista(id_usuario)
        return jsonify({
            'informacion' : datos
        })
   

    def leer_notificacion(self,id):
        notificacion = Noticacion()

        leer = notificacion.cambiar_estado(id)
        return jsonify({
                'leer':leer
            })
    
    def eliminar_notificacion(self,id):
        notificacion = Noticacion()

        eliminar = notificacion.eliminar_notificacion(id)

        return jsonify({
            'eliminar':eliminar
        })
    
    def obtener_numero_de_notificacion(self):
        usuario : dict = get_jwt_identity()
        id_usuario = usuario.get('id')

        notificacion = Noticacion()

        cantidad = notificacion.cantidad_notificaciones(id_usuario)[0]

        return jsonify({
            'numero_notificaciones': cantidad
        })
        


    

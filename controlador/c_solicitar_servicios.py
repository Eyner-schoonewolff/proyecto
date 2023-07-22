from flask import request, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from seguridad.Model_solicitar_servicio import Solicitar
from decorador.decoradores import *
from flask_jwt_extended import get_jwt_identity


class Solicitar_controlador():
    def servicio(self):
        identificadores = get_jwt_identity()
        id_usuario=identificadores.get('id')
        nombre = identificadores.get('username')
        tipo = identificadores.get('tipo_usuario')

        if request.method=='GET':
            return {'nombre':nombre,'tipo':tipo}
        
        fecha = request.form['fecha']
        hora = request.form['hora']
        contratista = request.form['contratista']
        problema = request.form['problema']
        tipo_contratista = request.form['servicio']

        file = request.files.get('evidencia')

        if not (file is None):
            filename = secure_filename(file.filename)
            # Capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
            extension = os.path.splitext(filename)[1]
            nuevo_nombre_file = str(uuid.uuid4()) + extension
            upload_path = os.path.join('static/img', nuevo_nombre_file)
            file.save(upload_path)
        else:
            nuevo_nombre_file = ""

        solicitar = Solicitar(fecha=fecha,
                              hora=hora,
                              contratista=contratista,
                              tipo_contratista=tipo_contratista,
                              evidencia=nuevo_nombre_file,
                              problema=problema,
                              id_usuario=id_usuario
                              )

        # valor = solicitar.agregar()
        valor=True
        if valor:
            return {"numero": 1}
        else:
            return {"numero": 0}

    def cancelar(self, id):
        identificadores = get_jwt_identity()
        tipo_usuario = identificadores.get('tipo_usuario')
        eliminar_solicitud = Solicitar()

        if eliminar_solicitud.eliminar(id=id) and tipo_usuario != 'Admin':
            return redirect(url_for('menus.consultar'))
        else:
            eliminar_solicitud.eliminar(id=id)
            return redirect(url_for('menus.consultar_admin'))

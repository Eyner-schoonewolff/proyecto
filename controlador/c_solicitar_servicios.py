from flask import request, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from seguridad.Model_solicitar_servicio import Solicitar
from decorador.decoradores import *
from flask_jwt_extended import get_jwt_identity
from PIL import Image
import base64
import imghdr
import io


class Solicitar_controlador():
    def servicio(self):
        identificadores = get_jwt_identity()
        id_usuario = identificadores.get('id')
        nombre = identificadores.get('username')
        tipo = identificadores.get('tipo_usuario')

        if request.method == 'POST':
            json = request.get_json()
            fecha = json['fecha']
            hora = json['hora']
            contratista = json['contratista']
            problema = json['problema']
            tipo_contratista = json['servicio']
            file = json['evidencia']

            print(file)
            if file:
                image = self.base64_to_image(file)
                extension = self.get_base64_extension(file)
                nuevo_nombre_file = str(uuid.uuid4()) + extension
                upload_path = os.path.join('static/img', nuevo_nombre_file)
                # Guarda los datos binarios en el archivo en el sistema de archivos.
                with open(upload_path, 'wb') as f:
                    f.write(image)
            else:
                nuevo_nombre_file = ""

            print(nuevo_nombre_file)
            solicitar = Solicitar(fecha=fecha,
                                  hora=hora,
                                  contratista=contratista,
                                  tipo_contratista=tipo_contratista,
                                  evidencia=nuevo_nombre_file,
                                  problema=problema,
                                  id_usuario=id_usuario
                                  )
            # valor = solicitar.agregar()
            valor = True

            if valor:
                return {"numero": 1}
            else:
                return {"numero": 0}
        else:
            return {'nombre': nombre, 'tipo': tipo}

    def cancelar(self, id):
        identificadores = get_jwt_identity()
        tipo_usuario = identificadores.get('tipo_usuario')
        eliminar_solicitud = Solicitar()

        if eliminar_solicitud.eliminar(id=id) and tipo_usuario != 'Admin':
            return redirect(url_for('menus.consultar'))
        else:
            eliminar_solicitud.eliminar(id=id)
            return redirect(url_for('menus.consultar_admin'))

    def base64_to_image(self, base64_string):
        # Elimina la parte inicial del string de Base64 para obtener solo los datos binarios.
        encoded = base64_string.split(',', 1)
        # Decodifica el string Base64 a datos binarios.
        decoded_data = base64.b64decode(encoded)
        return decoded_data

    def get_base64_extension(self, base64_string):
        # Analiza el string Base64 para extraer la extensión del archivo.
        metadata = base64_string.split(',', 1)
        if 'image/jpeg' in metadata:
            return '.jpg'
        elif 'image/png' in metadata:
            return '.png'

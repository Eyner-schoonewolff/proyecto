from flask import request
import os
import uuid
from seguridad.Model_solicitar_servicio import Solicitar
from decorador.decoradores import *
from flask_jwt_extended import get_jwt_identity
from PIL import Image
import base64
from io import BytesIO


class Solicitar_controlador():

    def guardar_imagen(self, file):
        image = self.base64_to_image(file)
        extension = self.get_base64_extension(image)
        nuevo_nombre_file = str(uuid.uuid4()) + '.' + extension
        upload_path = os.path.join('evidencias/img', nuevo_nombre_file)
        # Guarda los datos binarios en el archivo en el sistema de archivos.
        image.save(upload_path)

        return nuevo_nombre_file

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


            if file:
                nuevo_nombre_file=self.guardar_imagen(file)
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
            
            valor = solicitar.agregar()

            if valor:
                return {"numero": 1}
            else:
                return {"numero": 0}
        else:
            return {'nombre': nombre, 'tipo': tipo}

    def base64_to_image(self, base64_string: str):
        bytes_image = base64.b64decode(base64_string.split(",")[1])
        image = Image.open(BytesIO(bytes_image))
        return image
    
    def get_base64_extension(self, img: str):
        img_format = img.format.lower()
        return img_format


    def cancelar(self, id):
        identificadores = get_jwt_identity()
        tipo_usuario = identificadores.get('tipo_usuario')
        eliminar_solicitud = Solicitar()

        if eliminar_solicitud.eliminar(id=id) and tipo_usuario != 'Admin':
            return redirect(url_for('menus.consultar'))
        else:
            eliminar_solicitud.eliminar(id=id)
            return redirect(url_for('menus.consultar_admin'))

 

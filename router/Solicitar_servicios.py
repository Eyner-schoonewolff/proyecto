from flask import Blueprint, request, session, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from seguridad.Model_solicitar_servicio import Solicitar
from decorador.decoradores import  *


solicitar_servi = Blueprint('solicitar_servi', __name__, static_url_path='/static',
                            template_folder="templates")


@solicitar_servi.route("/solicitar_serv", methods=["POST"])
def solicitar_():
    logueado = session.get('login', False)
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    tipo_contratista = request.form.get('servicio')
    contratista = request.form.get('contratista')
    problema = request.form.get('problema')

    if not logueado:
        return redirect(url_for('login.index'))

    file = request.files.get('evidencia')
    if not(file is None):
        filename = secure_filename(file.filename)
        # Capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
        extension = os.path.splitext(filename)[1]
        nuevo_nombre_file = str(uuid.uuid4()) + extension
        upload_path = os.path.join('static/img', nuevo_nombre_file)
        file.save(upload_path)
    else:
        nuevo_nombre_file=""


    solicitar = Solicitar(fecha=fecha,
                          hora=hora,
                          contratista=contratista,
                          tipo_contratista=tipo_contratista,
                          evidencia=nuevo_nombre_file,
                          problema=problema
                          )

    valor = solicitar.agregar()
    if valor:
        return {"numero": 1}
    else:
        return {"numero": 0}


@solicitar_servi.route("/eliminar_solicitud/<id>", methods=['GET'])
@login_required_home
def eliminar_(id):
    tipo_usuario = session.get('tipo_usuario')

    eliminar_solicitud = Solicitar()

    if eliminar_solicitud.eliminar(id=id) and tipo_usuario!='Admin':
        return redirect(url_for('menus.consultar'))
    else:
        eliminar_solicitud.eliminar(id=id)
        return redirect(url_for('menus.consultar_admin'))


from flask import Blueprint, request, session, redirect, url_for, flash
from plyer import notification
import os
import uuid
from werkzeug.utils import secure_filename
from seguridad.Model_solicitar_servicio import Solicitar
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

    file = request.files['evidencia']
    # Nombre original del archivo
    filename = secure_filename(file.filename)
    # capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
    extension = os.path.splitext(filename)[1]

    nuevo_nombre_file = str(uuid.uuid4()) + extension

    upload_path = os.path.join('static/img', nuevo_nombre_file)

    file.save(upload_path)

    solicitar = Solicitar(fecha=fecha, hora=hora, tipo_contratista=tipo_contratista,
                          contratista=contratista,evidencia=nuevo_nombre_file, problema=problema)

    valor = solicitar.agregar()

    if valor:
        return {"numero": 1}
    else:
        return {"numero": 0}


@solicitar_servi.route("/eliminar_solicitud/<id>", methods=['GET', 'DELETE'])
def eliminar_(id):
    logueado = session.get('login', False)

    if not logueado:
        return redirect(url_for('login.index'))

    eliminar_solicitud = Solicitar()

    if eliminar_solicitud.eliminar(id=id):
        return redirect(url_for('menus.consultar'))

    return flash(message='No se pudo eliminar')

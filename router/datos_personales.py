from flask import Blueprint, request, session,redirect, url_for
from seguridad.datos_usuario import DatosUsuario

datos_personales = Blueprint('datos_personales', __name__, static_url_path='/static',
                             template_folder="templates")


@datos_personales.route('/auth_actualizar', methods=['POST'])
def auth():
    logueado = session.get('login', False)

    json = request.get_json()
    nombre = json['nombre']
    numeroCelular = json['numeroCelular']
    direccion = json['direccion']
    id_udp = session.get('id_udp')

    if not logueado:
        return redirect(url_for('login.index'))

    datos_usuario = DatosUsuario()

    datos_usuario.actualizar(nombre, numeroCelular, direccion, id_udp)

    return {'actualizar': True, 'home': '/actualizar'}

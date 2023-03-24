from flask import Blueprint, request, session, render_template, redirect, url_for
from seguridad.datos_usuario import DatosUsuario

datos_personales = Blueprint('datos_personales', __name__, static_url_path='/static',
                             template_folder="templates")


@datos_personales.route("/actualizar")
def actualizar():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)
    id = session.get('id')

    if not logueado:
        return redirect(url_for('login.index'))

    datos_usuario = DatosUsuario()

    ocupaciones = datos_usuario.ocupaciones()

    session['login'] = True
    usuario = datos_usuario.obtener(id)

    session['username'] = usuario['nombre_completo']
    session['numero_celular'] = usuario['numero_celular']
    session['direccion'] = usuario['direccion']

    return render_template(
        "actualizar.html",
        nombre=nombre_usuario,
        tipo=tipo_usuario,
        email=session.get('email'),
        numero=usuario['numero_celular'],
        numero_documento=usuario['numero_documento'],
        direccion=usuario['direccion'],
        ocupacion=usuario['ocupaciones'],
        ocupaciones_disponibles=ocupaciones
    )



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

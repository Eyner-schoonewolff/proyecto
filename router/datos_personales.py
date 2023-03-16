from flask import Blueprint, request, session, render_template, redirect, url_for
from seguridad.datos_usuario import DatosUsuario

datos_personales = Blueprint('datos_personales', __name__, static_url_path='/static',
                             template_folder="templates")


@datos_personales.route("/home")
def home():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)
    
    if not logueado:
        return redirect(url_for('login.index'))
    

    datos_usuario = DatosUsuario()

    session['login'] = True
    usuario = datos_usuario.obtener()
    return render_template("home.html", nombre=nombre_usuario, tipo=tipo_usuario, email=session.get('email'),
                           numero=usuario['numero_celular'], numero_documento=usuario['numero_documento'],
                           direccion=usuario['direccion'],ocupacion=usuario['ocupaciones'])


@datos_personales.route('/auth_actualizar', methods=['POST'])
def auth():
    json = request.get_json()

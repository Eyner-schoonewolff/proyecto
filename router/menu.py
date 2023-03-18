from flask import Blueprint, render_template, redirect, url_for, session
from seguridad.datos_usuario import DatosUsuario
from seguridad.solicitud import ConsultarSolicitud

menus = Blueprint('menus', __name__, static_url_path='/static',
                  template_folder="templates")


@menus.route('/home')
def home():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)
    if not logueado:
        return redirect(url_for('login.index'))

    return render_template("home.html", nombre=nombre_usuario,
                           tipo=tipo_usuario)


@menus.route("/solicitar")
def solicitar():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')

    logueado = session.get('login', False)

    if not logueado:
        return redirect(url_for('login.index'))
    return render_template("solicitar.html", nombre=nombre_usuario,
                           tipo=tipo_usuario, email=session.get('email'),
                            numero=session.get('numero_celular'))


@menus.route("/consultar")
def consultar():
    id_usuario=session.get('id')
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)


    if not logueado:
        return redirect(url_for('login.index'))
    
    consultar=ConsultarSolicitud()

    
    return render_template("consultar.html", nombre=nombre_usuario,
                           tipo=tipo_usuario,consultas= consultar.contratista(id_usuario))


@menus.route("/agregar")
def agregar():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)

    if not logueado:
        return redirect(url_for('login.index'))
    
    datos_usuario = DatosUsuario()

    ocupaciones=datos_usuario.ocupaciones()

    return render_template("agregar.html", nombre=nombre_usuario,
                           tipo=tipo_usuario,ocupaciones_disponibles=ocupaciones)

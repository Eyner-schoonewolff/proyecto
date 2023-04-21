from flask import Blueprint, render_template, redirect, url_for, request, session
from seguridad.datos_usuario import DatosUsuario

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


@menus.route("/actualizar")
def actualizar():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)
    id = session.get('id')

    if not logueado:
        return redirect(url_for('login.index'))

    datos_usuario = DatosUsuario()

    session['login'] = True
    usuario = datos_usuario.obtener(id)

    session['username'] = usuario['nombre_completo']
    session['numero_celular'] = usuario['numero_celular']
    session['direccion'] = usuario['direccion']

    return render_template(
        "informacion.html",
        nombre=nombre_usuario,
        tipo=tipo_usuario,
        email=session.get('email'),
        numero=usuario['numero_celular'],
        numero_documento=usuario['numero_documento'],
        direccion=usuario['direccion'],
        ocupacion=usuario['ocupaciones'],
    )


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
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)

    if not logueado:
        return redirect(url_for('login.index'))
    return render_template("consultar.html", nombre=nombre_usuario,
                           tipo=tipo_usuario)


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

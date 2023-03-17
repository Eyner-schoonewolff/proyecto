from flask import Blueprint, request, session, render_template, redirect, url_for
from seguridad.registrar import Usuario

registrar = Blueprint('registrar', __name__, static_url_path='/static',
                      template_folder="templates")


@registrar.route("/registrar")
def registro():
    logueado = session.get('login')
    if not logueado:
        return render_template("registrar.html")
    else:
        return redirect(url_for('login.home'))


@registrar.route("/auth_registro", methods=["POST"])
def auth():
    usuario_nuevo = request.get_json()
    email = str(usuario_nuevo['email'])
    contrasenia = usuario_nuevo['contrasenia']
    rol = int(usuario_nuevo['rol'])
    nombre = usuario_nuevo['nombre']
    tipo_documento = int(usuario_nuevo['tipo_documento'])
    numero_documento = int(usuario_nuevo['numero_documento'])
    celular = int(usuario_nuevo['celular'])
    direccion = str(usuario_nuevo['direccion'])


    registro = Usuario(email=email, contrasenia=contrasenia, rol=rol,
                       nombre=nombre, tipo_documento=tipo_documento, 
                       numero_documento=numero_documento,celular=celular,direccion=direccion)

    if registro.existe():
        return {"registro": False, "home": "/registrar"}
    else:
        registro.agregar()
        return {"registro": True, "home": "/registrar"}

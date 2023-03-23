from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from seguridad.datos_usuario import DatosUsuario
from seguridad.Model_solicitar_servicio import Solicitar

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


@menus.route("/solicitar", methods=['GET', 'POST'])
def solicitar_contratista():
    solicitar = Solicitar()
    contratista_consulta = []

    if request.method == 'POST':
        id = int(request.get_json()["id"])
        if not (id == 0):
            contratista_consulta.clear()
            contratistas = solicitar.consultar_contratista(id_ocupacion=id)
            contratista_consulta.append(contratistas)
            return jsonify({'contratista_consulta': contratista_consulta})
        return jsonify({'contratista_consulta': 0})

    else:
        nombre_usuario = session.get('username')
        tipo_usuario = session.get('tipo_usuario')

        logueado = session.get('login', False)

        if not logueado:
            return redirect(url_for('login.index'))

        return render_template("solicitar.html", nombre=nombre_usuario,
                               tipo=tipo_usuario, email=session.get('email'),
                               numero=session.get('numero_celular'), contratista_consulta=contratista_consulta)


@menus.route("/consultar")
def consultar():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)

    if not logueado:
        return redirect(url_for('login.index'))

    consultar = Solicitar()

    if consultar.contratista_():
        return render_template("consultar.html", nombre=nombre_usuario,
                               tipo=tipo_usuario, consulta_contratista=consultar.contratista_())

    return render_template("consultar.html", nombre=nombre_usuario,
                           tipo=tipo_usuario, consulta_cliente=consultar.cliente())


@menus.route("/evidencia/<id>")
def evidencia_solicitud(id):
    id_evidencia=int(id)
    logueado = session.get('login', False)
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')

    if not logueado:
        return redirect(url_for('login.index'))

    consultar = Solicitar()

    consulta=consultar.evidencia_(id=id_evidencia)

    return render_template("evidencias.html",nombre=nombre_usuario,tipo=tipo_usuario,informacion=consulta)


@menus.route("/agregar")
def agregar():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)

    if not logueado:
        return redirect(url_for('login.index'))

    datos_usuario = DatosUsuario()

    ocupaciones = datos_usuario.ocupaciones()

    return render_template("agregar.html", nombre=nombre_usuario,
                           tipo=tipo_usuario, ocupaciones_disponibles=ocupaciones)

from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, flash
from seguridad.Model_solicitar_servicio import Solicitar
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

    if not tipo_usuario == 'Contratista':
        return render_template("home.html", nombre=nombre_usuario,
                               tipo=tipo_usuario)
    consultar = Solicitar()

    id = session.get('id')
    notificacion_ = consultar.ultima_solicitud()
    if notificacion_['id'] == id:
        flash(message="Nueva Solicitud de {}".format(
            notificacion_['nombre']), category="Contratista")

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
        id = session.get('id')
        notificacion_ = consultar.ultima_solicitud()
        if notificacion_['id'] == id:
            flash(message="Nueva Solicitud de {}".format(
                notificacion_['nombre']), category="Contratista")
        return render_template("consultar.html", nombre=nombre_usuario,
                               tipo=tipo_usuario, consulta_contratista=consultar.contratista_())

    return render_template("consultar.html", nombre=nombre_usuario,
                           tipo=tipo_usuario, consulta_cliente=consultar.cliente())


@menus.route("/actualizar_estado/<id>", methods=['POST', 'GET'])
def actualizar_estado(id):
    if request.method == 'POST':
        id_select = request.get_json()['id']
        actualizar = Solicitar()
        actualizar.actualizar_estado(id_estado=id_select, id_solicitud=id)
        return jsonify({"actualizar": True, "recargar": "/consultar"})

    return redirect(url_for('menus.consultar'))


@menus.route("/evidencia/<id>")
def evidencia_solicitud(id):
    id_evidencia = int(id)
    logueado = session.get('login', False)
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')

    if not logueado:
        return redirect(url_for('login.index'))

    consultar = Solicitar()

    consulta = consultar.evidencia_(id=id_evidencia)

    return render_template("evidencias.html", nombre=nombre_usuario, tipo=tipo_usuario, informacion=consulta)


@menus.route("/contacto")
def contacto():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)

    if not logueado:
        return redirect(url_for('login.index'))

    consultar = Solicitar()

    id = session.get('id')
    notificacion_ = consultar.ultima_solicitud()
    if notificacion_['id'] == id:
        flash(message="Nueva Solicitud de {}".format(
            notificacion_['nombre']), category="Contratista")

    return render_template("contacto.html", nombre=nombre_usuario,
                           tipo=tipo_usuario)


@menus.route("/calendario")
def calendario():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)

    if not logueado:
        return redirect(url_for('login.index'))

    consultar = Solicitar()

    return render_template("calendario.html", nombre=nombre_usuario,
                               tipo=tipo_usuario, consulta_contratista=consultar.contratista_())


@menus.route("/calificar")
def calificar():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)

    if not logueado:
        return redirect(url_for('login.index'))

    consultar = Solicitar()

    if consultar.contratista_():
        return render_template("calificacion.html", nombre=nombre_usuario,
                               tipo=tipo_usuario, consulta_contratista=consultar.contratista_())

    return render_template("calificacion.html", nombre=nombre_usuario,
                           tipo=tipo_usuario, consulta_contratista=consultar.cliente())


@menus.route("/guardar-calificacion", methods=['POST'])
def guardar_calificacion():
    json = request.get_json()
    id_solicitud = json['id_solicitud']
    id_tipo_usuario = json['id_tipo_usuario']
    calificacion = json['estrellas']
    observacion = json['observacion']

    datosUsuario = DatosUsuario()

    agregar = datosUsuario.calificacion(observaciones=observacion,
                                        estrellas=calificacion, id_solicitud=id_solicitud, id_usuario_calificacion=id_tipo_usuario)

    if agregar:
        return jsonify({"actualizar": True, "recargar": "/calificar"})

    return jsonify({"actualizar": False, "recargar": "/calificar"})

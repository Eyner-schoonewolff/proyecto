from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, flash
from seguridad.Model_solicitar_servicio import Solicitar
from seguridad.datos_usuario import DatosUsuario
from seguridad.perfiles import Perfiles
from seguridad.contacto import Contacto,ValidacionDatosContacto

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

    return render_template("home.html", nombre=nombre_usuario,
                           tipo=tipo_usuario)


@menus.route('/perfiles', methods=['GET'])
def perfiles():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)
    if not logueado:
        return redirect(url_for('login.index'))

    perfiles = Perfiles()
    if tipo_usuario=='Contratista':
        mostrar = perfiles.consulta_cliente()
    elif tipo_usuario=='Cliente':
        mostrar = perfiles.consulta_contratista()
    else:
        mostrar= perfiles.consulta_cliente(),perfiles.consulta_contratista()


    return render_template("perfiles.html",
                           nombre=nombre_usuario,
                           tipo=tipo_usuario,
                           perfiles_usuario=mostrar
                           )


@menus.route('/perfiles/<id>', methods=['POST'])
def perfiles_cliente(id):
    tipo_usuario = session.get('tipo_usuario')
    id_usuario = int(id)
    perfiles = Perfiles()
    datos_json = request.get_json()
    id_usuario_cliente = datos_json['id_usuario_cliente']
    tipo_usuario_cliente = datos_json['tipo_usuario']

    if tipo_usuario == 'Contratista':
        informacion_usuario = perfiles.calificaciones_cliente(id_usuario_cliente=id_usuario_cliente, id_usuario=id_usuario)
        promedio = perfiles.promedio_cliente(id_usuario_cliente=id_usuario_cliente, id_usuario=id_usuario)
    elif tipo_usuario == 'Cliente':
        informacion_usuario = perfiles.calificaciones_contratista(id_usuario_cliente=id_usuario_cliente, id_usuario=id_usuario)
        promedio = perfiles.promedio_contratista(id_usuario_cliente=id_usuario_cliente, id_usuario=id_usuario)
    else:
        if tipo_usuario_cliente == 'Cliente':
            informacion_usuario = perfiles.calificaciones_contratista(id_usuario_cliente=id_usuario_cliente, id_usuario=id_usuario)
            promedio = perfiles.promedio_contratista(id_usuario_cliente=id_usuario_cliente, id_usuario=id_usuario)
        else:
            informacion_usuario = perfiles.calificaciones_cliente(id_usuario_cliente=id_usuario_cliente, id_usuario=id_usuario)
            promedio = perfiles.promedio_cliente(id_usuario_cliente=id_usuario_cliente, id_usuario=id_usuario)

    return jsonify({'actualizar': True, 'datos': informacion_usuario, 'calificacion': promedio})



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

    if not logueado or tipo_usuario=='Admin':
        return redirect(url_for('login.index'))

    consultar = Solicitar()

    if tipo_usuario=='Cliente':
        return render_template("consultar.html", nombre=nombre_usuario,
                               tipo=tipo_usuario, consultar_cliente=consultar.cliente())
    else:
        return render_template("consultar.html", nombre=nombre_usuario,
                                tipo=tipo_usuario, consulta_contratista=consultar.contratista_())

@menus.route("/consultar_admin")
def consultar_admin():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)

    if not logueado:
        return redirect(url_for('login.index'))

    consultar = Solicitar()

    return render_template("consultar.html", nombre=nombre_usuario,
                               tipo=tipo_usuario,consulta_admin_cliente=consultar.admin_cliente(),consulta_admin_contratista=consultar.admin_contratista())


@menus.route("/actualizar_estado/<id>", methods=['POST'])
def actualizar_estado(id):
    # import pdb
    # pdb.set_trace()
    json=request.get_json()
    estado_actual = json['estado_actual']
    id_estado = json['id']

    if estado_actual=='Aceptada':
        actualizar = Solicitar(id_estado=id_estado,id_solicitud=id)
        actualizar.actualizar_estado()
        return jsonify({"actualizar": True})
    else:
        fecha = json['fecha']
        hora = json['hora']
        actualizar = Solicitar(fecha=fecha,hora=hora,id_estado=id_estado,id_solicitud=id)
        actualizar.actualizar_fecha_estado()
        return jsonify({"actualizar": True})


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

    contacto=Contacto()

    consulta=contacto.informacion_usuario_contacto()

    return render_template("contacto.html", nombre=nombre_usuario,
                           tipo=tipo_usuario,usuario=consulta)


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
                           tipo=tipo_usuario, consulta_cliente=consultar.cliente())


@menus.route("/guardar-calificacion", methods=['POST'])
def guardar_calificacion():
    json = request.get_json()
    observacion = json['observacion']
    calificacion = json['estrellas']
    id_solicitud = json['id_solicitud']
    tipo_usuario = json['id_tipo_usuario']

    solicitud = DatosUsuario()

    agregar = solicitud.calificar(observaciones=observacion,
                                  estrellas=calificacion,
                                  id_solicitud=id_solicitud,
                                  tipo_usuario=tipo_usuario,
                                  )

    if agregar:
        return jsonify({"actualizar": True, "recargar": "/calificar"})

    return jsonify({"actualizar": False, "recargar": "/calificar"})


@menus.route("/enviar_correos", methods=['POST'])
def enviar_correos():
    json = request.get_json()
    correo = json['correo']
    nombre = json['nombre']
    numero = json['numero']
    asunto = json['asunto']
    mensaje = json['mensaje']
    correo= Contacto(correo=correo,nombre=nombre,numero=numero,asunto=asunto,mensaje=mensaje)
    try:
        if correo.validacion_contacto():
            raise ValidacionDatosContacto('No se pudo enviar el correo, hubo acceso a los datos')

        if correo.enviar_correos():
            return jsonify({"actualizar": True,"endpoint":"/contacto",'mensaje':'Por favor espere la respuesta de serviciossbarranquilla@gmail.com'})
    
    except ValidacionDatosContacto as exepcion:
        return jsonify({'actualizar':False,"endpoint":"/contacto",'mensaje':str(exepcion),'titulo':'Ups... Hubo un problema con los datos'})
    
    except Exception as exepcion:
        return jsonify({'actualizar':False,"endpoint":"/contacto",'mensaje':str(exepcion),'titulo':'Lo lamentamos, hubo un problema con el sevridor...'})
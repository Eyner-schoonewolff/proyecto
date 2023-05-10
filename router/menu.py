from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from seguridad.Model_solicitar_servicio import Solicitar
from seguridad.datos_usuario import DatosUsuario
from seguridad.perfiles import Perfiles
from seguridad.contacto import Contacto, ValidacionDatosContacto
from decorador.decoradores import  *


menus = Blueprint('menus', __name__, static_url_path='/static',
                  template_folder="templates")


@menus.route('/home',endpoint='home')
@login_required_home
def home():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')

    if not tipo_usuario == 'Contratista':
        return render_template("home.html", nombre=nombre_usuario,
                               tipo=tipo_usuario)

    return render_template("home.html", nombre=nombre_usuario,
                           tipo=tipo_usuario)


@menus.route('/perfiles',endpoint='perfiles')
@login_required_home
def perfiles():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')

    perfiles = Perfiles()
    if tipo_usuario == 'Contratista':
        mostrar = perfiles.consulta_cliente()
    elif tipo_usuario == 'Cliente':
        mostrar = perfiles.consulta_contratista()
    else:
        mostrar = perfiles.consulta_cliente(), perfiles.consulta_contratista()

    return render_template("perfiles.html",
                           nombre=nombre_usuario,
                           tipo=tipo_usuario,
                           perfiles_usuario=mostrar
                           )


@menus.route('/perfiles/<id>',endpoint="perfiles_id", methods=['POST','GET'])
@proteccion_ruta
def perfiles_cliente(id):
    tipo_usuario = session.get('tipo_usuario')
    id_usuario = int(id)

    datos_json = request.get_json()
    id_usuario_cliente = datos_json['id_usuario_cliente']
    tipo_usuario_cliente = datos_json['tipo_usuario']

    perfiles = Perfiles(id_usuario_cliente, id_usuario)

    if tipo_usuario == 'Contratista':
        informacion_usuario = perfiles.calificaciones_cliente()
        promedio = perfiles.promedio_cliente()
    elif tipo_usuario == 'Cliente':
        informacion_usuario = perfiles.calificaciones_contratista()
        promedio = perfiles.promedio_contratista()
    else:
        if tipo_usuario_cliente == 'Cliente':
            informacion_usuario = perfiles.calificaciones_contratista()
            promedio = perfiles.promedio_contratista()
        else:
            informacion_usuario = perfiles.calificaciones_cliente()
            promedio = perfiles.promedio_cliente()

    return jsonify({'actualizar': True, 'datos': informacion_usuario, 'calificacion': promedio})


@menus.route("/solicitar", endpoint='solicitar', methods=['GET', 'POST'])
@login_required_home
@proteccion_ruta_admin
def solicitar_contratista():
    contratista_consulta = []
    if request.method == 'POST':
        id = int(request.get_json()["id"])
        if not (id == 0):
            solicitar = Solicitar(id_solicitud=id)
            contratista_consulta.clear()
            contratistas = solicitar.consultar_contratista()
            contratista_consulta.append(contratistas)
            return jsonify({'contratista_consulta': contratista_consulta})
        return jsonify({'contratista_consulta': 0})

    else:
        nombre_usuario = session.get('username')
        tipo_usuario = session.get('tipo_usuario')
        email=session.get('email')
        numero=session.get('numero_celular')

        return render_template("solicitar.html", 
                               nombre=nombre_usuario,
                               tipo=tipo_usuario, 
                               email=email,
                               numero=numero, 
                               contratista_consulta=contratista_consulta)


@menus.route("/consultar",endpoint='consultar')
@login_required_home
@proteccion_ruta_admin
def consultar():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')

    consultar = Solicitar()

    if tipo_usuario == 'Cliente':
        return render_template("consultar.html", nombre=nombre_usuario,
                               tipo=tipo_usuario, consultar_cliente=consultar.cliente())
    elif tipo_usuario == 'Contratista':
        return render_template("consultar.html", nombre=nombre_usuario,
                               tipo=tipo_usuario, consulta_contratista=consultar.contratista_())
    else:
        return redirect(url_for('menus.consultar_admin'))


@menus.route("/consultar/admin",endpoint='consultar_admin')
@login_required_home
@proteccion_acceso_usuarios
def consultar_admin():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')

    consultar = Solicitar()

    return render_template("consultar.html", nombre=nombre_usuario,
                           tipo=tipo_usuario, consulta_admin_cliente=consultar.admin_cliente(), consulta_admin_contratista=consultar.admin_contratista())


@menus.route("/actualizar_estado/<id>", methods=['POST'])
def actualizar_estado(id):
    json = request.get_json()
    estado_actual = json['estado_actual']
    id_estado = json['id']

    if estado_actual == 'Aceptada':
        actualizar = Solicitar(id_estado=id_estado, id_solicitud=id)
        actualizar.actualizar_estado()
        return jsonify({"actualizar": True})
    else:
        fecha = json['fecha']
        hora = json['hora']
        actualizar = Solicitar(fecha=fecha, hora=hora,
                               id_estado=id_estado, id_solicitud=id)
        actualizar.actualizar_fecha_estado()
        return jsonify({"actualizar": True})


@menus.route("/evidencia/<id>",endpoint='evidencias', methods=['GET'])
@login_required_home
@proteccion_ruta_admin
def evidencia_solicitud(id):
    id_evidencia = int(id)
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')

    consultar = Solicitar()

    consulta = consultar.evidencia_(id=id_evidencia)

    return render_template("evidencias.html", nombre=nombre_usuario, tipo=tipo_usuario, informacion=consulta)


@menus.route("/contacto",endpoint='contacto')
@login_required_home
@proteccion_ruta_admin
def contacto():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')

    contacto = Contacto()

    consulta = contacto.informacion_usuario_contacto()

    return render_template("contacto.html", nombre=nombre_usuario,
                            tipo=tipo_usuario, usuario=consulta)
   


@menus.route("/calendario",endpoint='calendario')
@login_required_home
@proteccion_ruta_admin
def calendario():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')

    consultar = Solicitar()

    return render_template("calendario.html", nombre=nombre_usuario,
                            tipo=tipo_usuario, consulta_contratista=consultar.contratista_())



@menus.route("/calificar",endpoint='calificar')
@login_required_home
@proteccion_ruta_admin
def calificar():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
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
    tipo_usuario_calificar = json['id_tipo_usuario']

    solicitud = DatosUsuario(
        observaciones=observacion,
        estrellas=calificacion,
        id_solicitud=id_solicitud,
        tipo_usuario_calificar=tipo_usuario_calificar,
    )

    agregar = solicitud.calificar()
                                  
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

    correo = Contacto(correo=correo, nombre=nombre,
                      numero=numero, asunto=asunto, mensaje=mensaje)
    try:
        if correo.validacion_contacto():
            raise ValidacionDatosContacto(
                'No se pudo enviar el correo, hubo acceso a los datos')

        if correo.enviar_correos():
            return jsonify({"actualizar": True, "endpoint": "/contacto", 'mensaje': 'Por favor espere la respuesta de serviciossbarranquilla@gmail.com'})

    except ValidacionDatosContacto as exepcion:
        return jsonify({'actualizar': False, "endpoint": "/contacto", 'mensaje': str(exepcion), 'titulo': 'Ups... Hubo un problema con los datos'})

    except Exception as exepcion:
        return jsonify({'actualizar': False, "endpoint": "/contacto", 'mensaje': str(exepcion), 'titulo': 'Lo lamentamos, hubo un problema con el sevridor...'})


@menus.route('/perfiles_contra',endpoint='consultar_contratista')
@login_required_home
@proteccion_ruta_admin
def perfiles_contra():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')

    return render_template("perfiles_contratistas.html", nombre=nombre_usuario,
                           tipo=tipo_usuario,)

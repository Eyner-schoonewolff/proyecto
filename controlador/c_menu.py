from flask import render_template, redirect, url_for, session, request, jsonify
from seguridad.Model_solicitar_servicio import Solicitar
from seguridad.datos_usuario import DatosUsuario
from seguridad.perfiles import Perfiles
from seguridad.contacto import Contacto, ValidacionDatosContacto
from decorador.decoradores import *
from flask_jwt_extended import get_jwt_identity, jwt_required
from seguridad.login import *


class Menu_controlador():

    def home(self):
        identificadores = get_jwt_identity()
        nombre = identificadores.get('username')
        tipo = identificadores.get('tipo_usuario')

        if not nombre == 'Contratista':

            return jsonify({'nombre': nombre, 'tipo': tipo})

        return jsonify({'nombre': nombre, 'tipo': tipo})

    # metodo get, consulta informacion de los usuarios contratista o cliente

    def perfiles(self):

        identificadores = get_jwt_identity()

        nombre = identificadores.get('username')
        tipo_usuario = identificadores.get('tipo_usuario')

        perfiles = Perfiles()

        if tipo_usuario == 'Contratista':
            mostrar = perfiles.consulta_cliente()

        elif tipo_usuario == 'Cliente':
            mostrar = perfiles.consulta_contratista()
        else:
            mostrar = perfiles.consulta_cliente(), perfiles.consulta_contratista()

        return jsonify({'template': "/perfiles.html",
                        'nombre': nombre,
                        'tipo': tipo_usuario,
                        'perfiles_usuario': mostrar})

    def perfiles_cliente(self, id):

        identificadores = get_jwt_identity()

        tipo_usuario = identificadores.get('tipo_usuario')

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

    def solicitar_contratista(self):
        contratista_consulta = []
        if request.method == 'POST':
            id = int(request.get_json()["id"])
            if not (id == 0):
                solicitar = Solicitar(id_solicitud=id)
                contratista_consulta.clear()
                contratistas = solicitar.consultar_contratista()
                contratista_consulta.append(contratistas)
                print(contratistas)
                return jsonify({'contratista_consulta': contratista_consulta})
            return jsonify({'contratista_consulta': 0})


    def consultar(self):
        identificadores = get_jwt_identity()

        nombre = identificadores.get('username')
        tipo_usuario = identificadores.get('tipo_usuario')
        id = identificadores.get('id')

        consultar = Solicitar(id_usuario=id)

        if tipo_usuario == 'Cliente':
            return jsonify({'template': 'consultar.html', 'nombre': nombre, 'tipo': tipo_usuario, 'consultar_cliente': consultar.cliente()})
        elif tipo_usuario == 'Contratista':
            return jsonify({'template': 'consultar.html', 'nombre': nombre, 'tipo': tipo_usuario, 'consulta_contratista': consultar.contratista_()})

        else:
            return redirect(url_for('menus.consultar_admin'))

    def consultar_admin(self):
        identificadores = get_jwt_identity()

        nombre = identificadores.get('username')
        tipo_usuario = identificadores.get('tipo_usuario')

        consultar = Solicitar()

        return jsonify({'template': 'consultar.html', 'nombre': nombre, 'tipo': tipo_usuario, 'consulta_admin_cliente': consultar.admin_cliente(), 'consulta_admin_contratista': consultar.admin_contratista()})

    def consultar_estado(self, id):
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

    def evidencia(self, id):
        identificadores = get_jwt_identity()
        id_evidencia = int(id)

        nombre = identificadores.get('username')
        tipo_usuario = identificadores.get('tipo_usuario')

        consultar = Solicitar()

        consulta = consultar.evidencia_(id=id_evidencia)

        return jsonify({'template': 'evidencias.html', 'nombre': nombre, 'tipo': tipo_usuario, 'informacion': consulta})

    def contacto(self):
        identificadores = get_jwt_identity()

        id = identificadores.get('id')
        nombre = identificadores.get('username')
        tipo_usuario = identificadores.get('tipo_usuario')

        contacto = Contacto(id_usuario=id)

        consulta = contacto.informacion_usuario_contacto()

        return jsonify({'template': 'contacto.html', 'nombre': nombre, 'tipo': tipo_usuario, 'usuario': consulta})

    def calendario(self):

        identificadores = get_jwt_identity()

        nombre = identificadores.get('username')
        tipo_usuario = identificadores.get('tipo_usuario')

        consultar = Solicitar()

        return jsonify({'template': 'calendario.html', 'nombre': nombre, 'tipo': tipo_usuario, 'consulta_contratista': consultar.contratista_()})

    def calificar(self):
        identificadores = get_jwt_identity()
        nombre = identificadores.get('username')

        tipo_usuario = identificadores.get('tipo_usuario')

        id = identificadores.get('id')

        consultar = Solicitar(id_usuario=id)

        if consultar.contratista_():
            return jsonify({'template': 'calificacion.html', 'nombre': nombre, 'tipo': tipo_usuario, 'consulta_contratista': consultar.contratista_()})

        return jsonify({'template': 'calificacion.html', 'nombre': nombre, 'tipo': tipo_usuario, 'consulta_cliente': consultar.cliente()})

    def guardar_calificacion(self):
        json = request.get_json()
        identificadores = get_jwt_identity()


        id = identificadores.get('id')
        observacion = json['observacion']
        calificacion = int(json['estrellas'])
        id_solicitud = int(json['id_solicitud'])
        tipo_usuario_calificar = int(json['id_tipo_usuario'])

        solicitud = DatosUsuario(
            observaciones=observacion,
            estrellas=calificacion,
            id_solicitud=id_solicitud,
            tipo_usuario_calificar=tipo_usuario_calificar,
            id_usuario=id
        )

        agregar = solicitud.calificar()

        if agregar:
            return jsonify({"actualizar": True, "recargar": "../templates/calificacion.html"})

        return jsonify({"actualizar": False, "recargar": "../templates/calificacion.html"})

    def enviar_correos(self):
        json = request.get_json()
        identificadores = get_jwt_identity()

        correo = json['correo']
        nombre = json['nombre']
        numero = json['numero']
        asunto = json['asunto']
        mensaje = json['mensaje']
        tipo_usuario=identificadores.get('tipo_usuario')
        id = identificadores.get('id')

        correo = Contacto(correo=correo, nombre=nombre,
                          numero=numero, asunto=asunto, mensaje=mensaje,tipo_usuario=tipo_usuario,id_usuario=id)
        try:
            if correo.validacion_contacto():
                raise ValidacionDatosContacto(
                    'No se pudo enviar el correo, hubo acceso a los datos')

            if correo.enviar_correos():
                return jsonify({"actualizar": True, "endpoint": "../templates/contacto.html", 'mensaje': 'Por favor espere la respuesta de serviciossbarranquilla@gmail.com'})

        except ValidacionDatosContacto as exepcion:
            return jsonify({'actualizar': False, "endpoint": "../templates/contacto.html", 'mensaje': str(exepcion), 'titulo': 'Ups... Hubo un problema con los datos'})

        except Exception as exepcion:
            return jsonify({'actualizar': False, "endpoint": "../templates/contacto.html", 'mensaje': str(exepcion), 'titulo': 'Lo lamentamos, hubo un problema con el sevridor...'})

    def perfiles_contratista(self):
        identificadores = get_jwt_identity()
        nombre = identificadores.get('username')
        tipo_usuario=identificadores.get('tipo_usuario')

        return jsonify({'template': '/perfiles_contratistas.html', 'nombre': nombre, 'tipo': tipo_usuario})

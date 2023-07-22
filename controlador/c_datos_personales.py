from flask import request, session, render_template, jsonify
from seguridad.datos_usuario import DatosUsuario, DatoUnicoEmail, CorreoInvalido
from seguridad.Model_solicitar_servicio import *
from decorador.decoradores import *
import json
from flask_jwt_extended import get_jwt_identity, jwt_required


class Datos_personales_controlador():
    def __init__(self) -> None:
        pass

    def c_actualizar_ocupaciones(self):

        identificadores = get_jwt_identity()
        id = identificadores.get('id')
        nombre = identificadores.get('username')
        tipo = identificadores.get('tipo_usuario')
        email = identificadores.get('email')

        datos_usuario = DatosUsuario(id_usuario=id)

        ocupaciones = datos_usuario.ocupaciones()

        session['login'] = True

        usuario = datos_usuario.obtener()

        if tipo == 'Contratista':
            return jsonify({'datos':
                            [
                                {'nombre': nombre,
                                 'tipo': tipo,
                                 'email': email,
                                 'numero_documento': usuario['numero_documento'],
                                 'numero': usuario['numero_celular'],
                                 'descripcion': usuario['descripcion'],
                                 'direccion':usuario['direccion'],
                                 'ocupacion':usuario['ocupaciones'],
                                 'ocupaciones_disponibles':ocupaciones
                                 }
                            ]})
        else:
            return jsonify({'datos':
                            [
                                {'nombre': nombre,
                                 'tipo': tipo,
                                 'email': email,
                                 'numero_documento': usuario['numero_documento'],
                                 'numero': usuario['numero_celular'],
                                 'descripcion': usuario['descripcion'],
                                 'direccion':usuario['direccion'],
                                 }
                            ]})

    def actualizar_admin(self):
        nombre_usuario = session.get('username')
        tipo_usuario = session.get('tipo_usuario')

        if request.method == 'POST':
            email = request.get_json()["email"]
            consultar = DatosUsuario(verificacion_email=email)
            informacion = consultar.informacion_usuario()

            return jsonify({'datos': informacion})
        else:
            return jsonify({'templates': '/actualizar.html', 'nombre': nombre_usuario, 'tipo': tipo_usuario})

    def actualizar_email(self):
        json = request.get_json()
        email_actual = json['email_actual']
        email_nuevo = json['email_nuevo']

        datosUsuario = DatosUsuario(
            email_actual=email_actual, email_nuevo=email_nuevo)
        try:
            if datosUsuario.existe_correo():
                raise DatoUnicoEmail(
                    f"No se puede actualizar,{email_nuevo} ya que este correo se encuentra registrado, intente con otro diferente ")

            elif not (datosUsuario.validar_correo_electronico()):
                raise CorreoInvalido(
                    f"No se puede actualizar,{email_nuevo} No es un correo valido"
                )

            elif datosUsuario.actualizar_email():
                return jsonify({"actualizacion": True, "mensaje": f"Se ha actualizado el correo {email_nuevo} correctamente", "home": "/actualizar/admin"})

        except DatoUnicoEmail as mensaje:
            return jsonify({"actualizacion": False, "mensaje_excepcion": str(mensaje), "home": "/actualizar/admin"})

        except CorreoInvalido as mensaje:
            return jsonify({"actualizacion": False, "mensaje_excepcion": str(mensaje), "home": "/actualizar/admin"})

        except Exception as error:
            return jsonify({"actualizacion": False, "mensaje_excepcion": str(error), "home": "/actualizar/admin"})

    def actualizar_informacion(self):
        json = request.get_json()
        identificadores = get_jwt_identity()
        nombre = json['nombre']
        numeroCelular = json['numeroCelular']
        direccion = json['direccion']
        id_udp = identificadores.get('id_udp')
        descripcion = json['descripcion']

        datos_usuario = DatosUsuario()

        datos_usuario.actualizar(
            nombre, numeroCelular, direccion, descripcion, id_udp)

        return {'actualizar': True, 'home': '../templates/actualizar.html'}

    def ocupaciones_contratista(self):
        identificadores = get_jwt_identity()

        id = identificadores.get('id')

        datos_usuario = DatosUsuario()
        datos = datos_usuario.ocupaciones_contratista(id)

        if (len(datos) > 0):
            return {"numero": 1, "datos": datos}
        else:
            return {"numero": 2}

    def agregar_ocupacion(self):
        identificadores = get_jwt_identity()
        id = identificadores.get('id')
        json_ = request.get_json()
        ocupaciones = json_['datos']
        datos_usuario = DatosUsuario()
        datos = datos_usuario.ocupaciones_contratista(id)
        datos_eliminado = datos_usuario.ocupaciones_eliminadas(id)

        cadena = ''
        if (len(datos) == 0):
            for i in range(0, len(ocupaciones)):
                cadena += '('+str(id) + ',' + ocupaciones[i]+'),'

            cadena = cadena[:-1]
            datos_usuario.agregar_ocupaciones(cadena)
            return {"numero": 1, 'home': '/actualizar'}

        elif (len(datos) > 0):
            array = []
            array_ocu = []
            array_eli = []
            for i in datos:
                array.append(i['id'])

            for i in range(0, len(ocupaciones)):
                array_ocu.append(json.loads(ocupaciones[i]))

            for i in datos_eliminado:
                array_eli.append(i['id'])

            # insertar nuevas ocupaciones
            cadena_a = ''
            for i in array_ocu:
                validar = i in array
                validar_e = i in array_eli
                if (validar == False and validar_e == False):
                    cadena += '('+str(id) + ',' + str(i)+'),'
                elif (validar == False and validar_e == True):
                    cadena_a += str(i)+','

            # Agregar
            if (cadena != ''):
                cadena = cadena[:-1]
                datos_usuario.agregar_ocupaciones(cadena)

            # Actualizar
            if (cadena_a != ''):
                cadena_a = cadena_a[:-1]
                datos_usuario.actualizar_ocupaciones(id, cadena_a)

            # eliminar ocupacion
            cadena_e = ''
            for i in array:
                validar_e = i in array_ocu
                if (validar_e == False):
                    cadena_e += str(i)+','
            if (cadena_e != ''):
                cadena_e = cadena_e[:-1]
                datos_usuario.eliminar_ocupaciones(id, cadena_e)

            return {"numero": 2, 'home': '/actualizar'}

    def informacion_contratista(self):
        identificadores = get_jwt_identity()
        nombre = identificadores.get('username')
        tipo = identificadores.get('tipo_usuario')
        datos_usuario = DatosUsuario()
        datos = datos_usuario.informacion_contratistas()
        return jsonify({'perfiles': datos, 'nombre': nombre, 'tipo': tipo})

    def eventos(self):
        identificadores = get_jwt_identity()
        id = identificadores.get('id')
        nombre = identificadores.get('username')
        tipo = identificadores.get('tipo_usuario')
        datos_usuario = DatosUsuario()
        datos = datos_usuario.eventos_contratistas(id)
        return jsonify({'eventos': datos, 'nombre': nombre, 'tipo': tipo})

    def datosestadistica(self):
        identificadores = get_jwt_identity()
        id = identificadores.get('id')
        datos_usuario = DatosUsuario()
        datos = datos_usuario.datos_solicitudes(id)
        return datos

    def datosestadisticaslinea(self):
        identificadores = get_jwt_identity()
        id = identificadores.get('id')
        datos_usuario = DatosUsuario()
        datos = datos_usuario.datosestadisticaslinea(id)
        return datos

    def datosestadisticastorta(self):
        identificadores = get_jwt_identity()
        id = identificadores.get('id')
        datos_usuario = DatosUsuario()
        datos = datos_usuario.datosestadisticastorta(id)
        return datos

    def header_usuarios(self):

        identificadores = get_jwt_identity()
        nombre = identificadores.get('username')
        tipo = identificadores.get('tipo_usuario')
        return {"tipo": tipo, "nombre": nombre}

    def ocupaciones_(self):
        datos_usuario = DatosUsuario()
        datos = datos_usuario.ocupaciones_()
        return {"datos": datos}

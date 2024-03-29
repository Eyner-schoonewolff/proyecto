from flask import Blueprint, request, session, render_template,jsonify
from seguridad.datos_usuario import DatosUsuario,DatoUnicoEmail,CorreoInvalido
from seguridad.Model_solicitar_servicio import *
from decorador.decoradores import  *
import json

datos_personales = Blueprint('datos_personales', __name__, static_url_path='/static',
                             template_folder="templates")


@datos_personales.route("/actualizar", endpoint='actualizar')
@login_required_home
def actualizar():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    
    datos_usuario = DatosUsuario()

    ocupaciones = datos_usuario.ocupaciones()

    session['login'] = True

    usuario = datos_usuario.obtener()

    session['username'] = usuario['nombre_completo']
    session['numero_celular'] = usuario['numero_celular']
    session['direccion'] = usuario['direccion']

    if tipo_usuario=='Contratista':
        session['descripcion'] = usuario['descripcion']
        return render_template(
            "actualizar.html",
            nombre=nombre_usuario,
            tipo=tipo_usuario,
            email=session.get('email'),
            numero=usuario['numero_celular'],
            numero_documento=usuario['numero_documento'],
            descripcion=usuario['descripcion'],
            direccion=usuario['direccion'],
            ocupacion=usuario['ocupaciones'],
            ocupaciones_disponibles=ocupaciones
        )
    else:
        return render_template(
            "actualizar.html",
            nombre=nombre_usuario,
            tipo=tipo_usuario,
            email=session.get('email'),
            numero=usuario['numero_celular'],
            numero_documento=usuario['numero_documento'],
            direccion=usuario['direccion'],
        )


@datos_personales.route("/actualizar/admin",endpoint='actualizar/admin' ,methods=['GET','POST'])
@login_required_home
@proteccion_acceso_usuarios
def actualizar_admin():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    
    if request.method == 'POST':
        email = request.get_json()["email"]
        consultar = DatosUsuario(verificacion_email=email)
        informacion=consultar.informacion_usuario()
        return jsonify({'datos': informacion})
    else:
        return render_template("actualizar.html",
        nombre=nombre_usuario,
        tipo=tipo_usuario)
    
@datos_personales.route("/actualizar/email_usuario",endpoint='actualizar/email_usuario', methods=['POST','GET'])
@proteccion_ruta
@proteccion_acceso_usuarios
def actualizar_email_usuario():
    json = request.get_json()
    email_actual=json['email_actual']
    email_nuevo=json['email_nuevo']
    
    datosUsuario=DatosUsuario(email_actual=email_actual,email_nuevo=email_nuevo)
    try:
        if datosUsuario.existe_correo():
            raise DatoUnicoEmail(
            f"No se puede actualizar,{email_nuevo} ya que este correo se encuentra registrado, intente con otro diferente ")
        
        elif not(datosUsuario.validar_correo_electronico()):
            raise CorreoInvalido(
                f"No se puede actualizar,{email_nuevo} No es un correo valido"
                )
        
        elif datosUsuario.actualizar_email():
            return jsonify({"actualizacion":True,"mensaje":f"Se ha actualizado el correo {email_nuevo} correctamente","home":"/actualizar/admin"})
    
    except DatoUnicoEmail as mensaje:
        return jsonify({"actualizacion":False,"mensaje_excepcion":str(mensaje),"home":"/actualizar/admin"})
    
    except CorreoInvalido as mensaje:
        return jsonify({"actualizacion":False,"mensaje_excepcion":str(mensaje),"home":"/actualizar/admin"})
    
    except Exception as error:
        return jsonify({"actualizacion":False,"mensaje_excepcion":str(error),"home":"/actualizar/admin"})
    



@datos_personales.route('/auth/actualizar', endpoint='auth/actualizar',methods=['POST','GET'])
@proteccion_ruta
def auth():
    json = request.get_json()
    nombre = json['nombre']
    numeroCelular = json['numeroCelular']
    direccion = json['direccion']
    id_udp = session.get('id_udp')
    descripcion = json['descripcion']

    datos_usuario = DatosUsuario()

    datos_usuario.actualizar(nombre, numeroCelular, direccion,descripcion, id_udp)

    return {'actualizar': True, 'home': '/actualizar'}


@datos_personales.route('/ocupaciones_contratista', endpoint='ocupaciones_contratista',methods=['GET'])
@proteccion_ruta_admin
def ocup():
    id = session.get('id')
    datos_usuario = DatosUsuario()
    datos = datos_usuario.ocupaciones_contratista(id)

    if(len(datos) > 0):
        return {"numero": 1,"datos": datos}
    else:
        return {"numero": 2}


@datos_personales.route('/agregar_ocupaciones', methods=['POST'])
def agregar():
    id = session.get('id')
    json_ = request.get_json()
    ocupaciones = json_['datos']
    datos_usuario = DatosUsuario()
    datos = datos_usuario.ocupaciones_contratista(id)
    datos_eliminado = datos_usuario.ocupaciones_eliminadas(id)
    
    cadena = ''
    if(len(datos) == 0):
        for i in range(0, len(ocupaciones)):
            cadena += '('+str(id) + ',' +ocupaciones[i]+'),'
           
        cadena = cadena[:-1]
        print(cadena)
        datos_usuario.agregar_ocupaciones(cadena)
        return {"numero": 1,'home': '/actualizar'}
    
    elif(len(datos) > 0):
        array = []
        array_ocu=[]
        array_eli=[]
        for i in datos:
            array.append(i['id'])
        
        for i in range(0, len(ocupaciones)):
            array_ocu.append(json.loads(ocupaciones[i]))
        
        for i in datos_eliminado:
            array_eli.append(i['id'])
        
        # insertar nuevas ocupaciones
        cadena_a='';  
        for i in array_ocu:
            validar = i in array
            validar_e = i in array_eli
            if(validar == False and validar_e == False):
                cadena += '('+str(id) + ',' +str(i)+'),'
            elif(validar == False and validar_e == True):
                cadena_a += str(i)+','
        
        # Agregar
        if(cadena != ''):
            cadena = cadena[:-1]
            datos_usuario.agregar_ocupaciones(cadena)

        # Actualizar
        if(cadena_a != ''):
            cadena_a = cadena_a[:-1]
            datos_usuario.actualizar_ocupaciones(id,cadena_a)


        # eliminar ocupacion
        cadena_e=''
        for i in array:
            validar_e = i in array_ocu
            if(validar_e == False):
                cadena_e += str(i)+','
        if(cadena_e != ''):
            cadena_e = cadena_e[:-1]
            datos_usuario.eliminar_ocupaciones(id,cadena_e)
             
        return {"numero": 2,'home': '/actualizar'}
    
@datos_personales.route('/contratistas',endpoint='contratistas', methods=['GET'])
@proteccion_ruta_admin
def contra():
    datos_usuario = DatosUsuario()
    datos =datos_usuario.informacion_contratistas()
    return datos

@datos_personales.route('/eventos',endpoint='eventos', methods=['GET'])
@proteccion_ruta_admin
def event():
    id = session.get('id')
    datos_usuario = DatosUsuario()
    datos =datos_usuario.eventos_contratistas(id)
    return datos
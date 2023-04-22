from flask import Blueprint, request, session, render_template, redirect, url_for,flash,jsonify
from seguridad.datos_usuario import DatosUsuario,DatoUnicoEmail,CorreoInvalido
from seguridad.Model_solicitar_servicio import *
import json

datos_personales = Blueprint('datos_personales', __name__, static_url_path='/static',
                             template_folder="templates")


@datos_personales.route("/actualizar")
def actualizar():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)

    if not logueado or tipo_usuario=='Admin':
        return redirect(url_for('login.index'))
    
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


@datos_personales.route("/actualizar_admin", methods=['GET','POST'])
def actualizar_admin():
    nombre_usuario = session.get('username')
    tipo_usuario = session.get('tipo_usuario')
    logueado = session.get('login', False)

    if not logueado:
        return redirect(url_for('login.index'))
    
    if request.method == 'POST':
        email = request.get_json()["email"]
        consultar = DatosUsuario()
        informacion=consultar.informacion_usuario(email=email)
        return jsonify({'datos': informacion})
    else:
        return render_template("actualizar.html",
        nombre=nombre_usuario,
        tipo=tipo_usuario)
    
@datos_personales.route("/actualizar_email_usuario", methods=['POST'])
def actualizar_email_usuario():
    logueado = session.get('login', False)
    json = request.get_json()
    email_actual=json['email_actual']
    email_nuevo=json['email_nuevo']

    if not logueado:
        return redirect(url_for('login.index'))
    
    datosUsuario=DatosUsuario(email_actual=email_actual,email_nuevo=email_nuevo)
    try:
        if datosUsuario.existe_correo():
            raise DatoUnicoEmail(f"No se puede actualizar,{email_nuevo} ya que este correo se encuentra registrado, intente con otro diferente ")
        
        elif not(datosUsuario.validar_correo_electronico()):
            raise CorreoInvalido(f"No se puede actualizar,{email_nuevo} No es un correo valido")
        
        elif datosUsuario.actualizar_email():
            return jsonify({"actualizacion":True,"mensaje":f"Se ha actualizado el correo {email_nuevo} correctamente","home":"/actualizar_admin"})
    
    except DatoUnicoEmail as mensaje:
        return jsonify({"actualizacion":False,"mensaje_excepcion":str(mensaje),"home":"/actualizar_admin"})
    
    except CorreoInvalido as mensaje:
        return jsonify({"actualizacion":False,"mensaje_excepcion":str(mensaje),"home":"/actualizar_admin"})
    
    except Exception as error:
        return jsonify({"actualizacion":False,"mensaje_excepcion":str(error),"home":"/actualizar_admin"})



@datos_personales.route('/auth_actualizar', methods=['POST'])
def auth():
    logueado = session.get('login', False)

    json = request.get_json()
    nombre = json['nombre']
    numeroCelular = json['numeroCelular']
    direccion = json['direccion']
    id_udp = session.get('id_udp')
    descripcion = json['descripcion']

    if not logueado:
        return redirect(url_for('login.index'))

    datos_usuario = DatosUsuario()

    datos_usuario.actualizar(nombre, numeroCelular, direccion,descripcion, id_udp)

    return {'actualizar': True, 'home': '/actualizar'}


@datos_personales.route('/ocupaciones_contratista', methods=['GET'])
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
    
@datos_personales.route('/contratistas', methods=['GET'])
def contra():
    datos_usuario = DatosUsuario()
    datos =datos_usuario.informacion_contratistas()
    return datos

@datos_personales.route('/eventos', methods=['GET'])
def event():
    id = session.get('id')
    datos_usuario = DatosUsuario()
    datos =datos_usuario.Eventos_contratistas(id)
    return datos
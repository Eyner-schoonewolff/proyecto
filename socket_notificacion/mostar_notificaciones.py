from flask_socketio import SocketIO, emit,join_room,leave_room
from flask import session,request
from decorador.decoradores import  *
from seguridad.notificacion import Noticacion
socketio = SocketIO(cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

@socketio.on("join")
def on_join(data):
    user = data["username"]
    room = data["room"]
    print(f"client {user} wants to join: {room}")
    join_room(room)
    emit("join",{'id':room,'nombre':user},room = room)

@socketio.on('leave')
def leave_sesion(id):
    room = id
    print(f"Usuario con el id: {room} finalizo la sala")
    leave_room(room)
    emit("leave", data = id , room = id)

@socketio.on('mi_evento')
def handle_mi_evento(data):
    room = data["room"]
    join_room(room)
    emit('mi_evento',
         {'titulo':f'Nueva solicitud del usuario {data["nombre"]}',
          'horario': f'{data["fecha"]} - {data["hora"]}',
          'contenido': f"El usuario necesita de un {data['servicio_usuario']} para {data['problema']}",
            }
         ,room = room)
    
@socketio.on('numero_notificacion')
def conteo_notificacion(info):
    room = info
    join_room(room)
    notificacion = Noticacion()
    numero = notificacion.cantidad_notificaciones(room)[0]
    emit('numero_notificacion', {'cantidad':numero}, room=room)
    
 

from flask_socketio import SocketIO, emit,join_room,leave_room
from flask import session,request
from decorador.decoradores import  *

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
         {'servicio':data['servicio'],'nombre_servicio':data['nombre_servicio'],
          'hora':data['hora'],'fecha':data['fecha'],'problema':data['problema']}
         ,room = room)
    
 

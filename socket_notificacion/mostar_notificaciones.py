from flask_socketio import SocketIO, emit,join_room,leave_room
from flask import session,request
from flask_jwt_extended import get_jwt_identity, jwt_required
from decorador.decoradores import  *

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    print(username)
    print(room)
    join_room(room)
    emit('message', username + ' ha ingresado a la sala ' + room)

@socketio.on('mi_evento')
def handle_mi_evento(data):
    emit('mi_evento', data,room = int(data))
    



 


from functools import wraps
from flask import  redirect, url_for, jsonify, session,request
from seguridad.login import *
from flask_jwt_extended import get_jwt_identity,jwt_required
from functools import wraps
import jwt


def token_requeried(f):
    @wraps(f)
    def ruta_proteccion(*args, **kwargs):
        try:
             # Verifica el token aquí antes de obtener la identidad
            identificador: Dict = get_jwt_identity()
            token_id = identificador.get('id')
            print(token_id)
            if not token_id:
                return jsonify({'messague': 'Token is missing!'}), 403
            print(token_id)
        except jwt.ExpiredSignatureError:
            return jsonify({'messague': 'Token has expired'}), 401
        return f(*args, **kwargs)
    return ruta_proteccion


# def token_requeried(f):
#     @wraps(f)
#     def ruta_protecion(*args, **kwargs):
#         identificador:Dict = get_jwt_identity()
#         # token=request.args.get('token')
#         token_id=identificador.get('id')
#         if not token_id:
#             return jsonify({'messague':'Token is missing!'}),403
#         try:
#             print(token_id)
#         except:
#              return jsonify({'messague':'Token is invalid'}),403
#         return f(*args, **kwargs)
#     return ruta_protecion

def login_ruta_acceso(funcion_interna_home):
    def principal_acceso_funcion(*args, **kwargs):
        logueado = session.get('login')
        if logueado:
            return redirect(url_for('menus.home'))
        else:
            return funcion_interna_home(*args, **kwargs)
    return principal_acceso_funcion


def login_required_home(funcion_interna_home):
    def wrapper(*args, **kwargs):
        logueado = session.get('login')
        if logueado:
            return funcion_interna_home(*args, **kwargs)
        else:
            return redirect(url_for('login.inicio'))
    return wrapper


def proteccion_ruta_admin(funcion_proteccion):
    def ruta_protecion_admin(*args, **kwargs):
        tipo_usuario = session.get('tipo_usuario')
        if tipo_usuario == 'Admin':
            return redirect(url_for('menus.home'))
        else:
            return funcion_proteccion(*args, **kwargs)
    return ruta_protecion_admin

def proteccion_acceso_usuarios(funcion_proteccion):
    def ruta_protecion(*args, **kwargs):
        tipo_usuario = session.get('tipo_usuario')
        if tipo_usuario == 'Cliente' or tipo_usuario =='Contratista':
            return redirect(url_for('menus.home'))
        else:
            return funcion_proteccion(*args, **kwargs)
    return ruta_protecion


def login_required_login(func):
    def funcion_wrapper(*args, **kwargs):
        logueado = session.get('login')
        if logueado:
            return redirect(url_for('login.inicio'))
        else:
            return func(*args, **kwargs)
    return funcion_wrapper


def proteccion_ruta(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if request.method == 'POST':
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login.inicio'))
    return decorador

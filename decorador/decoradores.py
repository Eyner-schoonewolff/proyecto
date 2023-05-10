from flask import session, redirect, url_for, request
from functools import wraps


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

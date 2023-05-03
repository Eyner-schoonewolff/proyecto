from flask import session,redirect,url_for,request
from functools import wraps

def login_required_home(funcion_interna_home):
    def wrapper(*args, **kwargs):
        logueado = session.get('login')
        if logueado:
            return funcion_interna_home(*args, **kwargs)
        else:
            return redirect(url_for('login.index'))
    return wrapper

def login_required_login(func):
    def funcion_wrapper(*args, **kwargs):
        logueado = session.get('login')
        if logueado:
            return redirect(url_for('login.index'))
        else:
            return func(*args, **kwargs)
    return funcion_wrapper

def proteccion_ruta(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if request.method == 'POST':
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login.index'))
    return decorador
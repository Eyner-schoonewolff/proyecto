from flask import Flask
from router.router import login,login_manager
from socket_notificacion.mostar_notificaciones import socketio
from router.registrar import registrar
from router.datos_personales import datos_personales
from router.menu import menus
from router.Solicitar_servicios import solicitar_servi
from router.notificacion import notificacion
# Routes

app = Flask(__name__)


def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(login)
    app.register_blueprint(registrar)
    app.register_blueprint(datos_personales)
    app.register_blueprint(menus)
    app.register_blueprint(solicitar_servi)
    app.register_blueprint(notificacion)
    login_manager.init_app(app)
    socketio.init_app(app)

    return app
from flask import Flask
from router.router import login, login_manager
from router.registrar import registrar
from router.datos_personales import datos_personales
from router.menu import menus
from router.Solicitar_servicios import solicitar_servi
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta


app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})
jwt = JWTManager(app)
app.config['SECRET_KEY'] = 'secret_key_parking'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)


app.register_blueprint(login)
app.register_blueprint(registrar)
app.register_blueprint(datos_personales)
app.register_blueprint(menus)
app.register_blueprint(solicitar_servi)
login_manager.init_app(app)

if __name__ == "__main__":
    # app.register_error_handler(405, notFound)
    app.run(debug=True, port=3000)

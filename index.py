from flask import Flask
from router.router import login,login_manager
from router.registrar import registrar
from router.datos_personales import datos_personales

app = Flask(__name__)
app.register_blueprint(login)
app.register_blueprint(registrar)
app.register_blueprint(datos_personales)
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

if __name__ == "__main__":
    app.run(debug=True, port=3000)


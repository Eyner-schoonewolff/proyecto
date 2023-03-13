from flask import Flask
from router.router import login,login_manager
from router.registrar import registrar


app = Flask(__name__)
app.register_blueprint(login)
app.register_blueprint(registrar)
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

if __name__ == "__main__":
    app.run(debug=True, port=3000)


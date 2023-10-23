from __init__ import init_app
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config

app = Flask(__name__)

configuracion = config['development']

app = init_app(configuracion)

cors = CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(port=3000)

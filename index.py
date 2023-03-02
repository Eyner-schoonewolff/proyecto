from flask import Flask
from router.router import login,login_manager


app = Flask(__name__)
app.register_blueprint(login)
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

if __name__ == "__main__":
    app.run(debug=True, port=5000)


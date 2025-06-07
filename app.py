from flask import Flask
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

# Rutas
from routes.accounts_routes import *
from routes.users_routes import *
from routes.rentals_routes import *
from routes.profiles_routes import *
from routes.clients_routes import *

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(accounts)
app.register_blueprint(users)
app.register_blueprint(rentals)
app.register_blueprint(profiles)
app.register_blueprint(clients)

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada ...<h1>"

if __name__ == "__main__":
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host="0.0.0.0", port=5000, debug=True)
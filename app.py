from flask import Flask
from database import db
from sqlalchemy_utils import create_database, database_exists
from routes.route import blue_print
from flask_jwt_extended import JWTManager
import datetime
import os

app = Flask(__name__)


PWD = os.path.abspath(os.curdir)
DB_NAME = "database.sqlite3"
# connection string
DB_URL = f"sqlite:///{PWD}/{DB_NAME}"

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Coloco secret key
app.config["JWT_SECRET_KEY"] = "3st4-3s-M1-Cl4ave-Se3cr3ta"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(
    hours=12)  # Coloco el tiempo de expiracion del jwt token

# jwt

jwt = JWTManager(app)


# iniciamos la app
db.init_app(app)

# Registramos el blueprint

app.register_blueprint(blue_print)

# Creamos la Base de datos SI NO EXISTE LA CREA
with app.app_context():  # app context para la current app
    if not database_exists(DB_URL):
        create_database(DB_URL)  # crea bdd
    db.create_all()  # crea todas las tablas

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")

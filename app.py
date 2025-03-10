from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# Mando a llamar mis archivos {carpeta}.{archivo}
from General.autores import Autor, AutorResource, AutorListResource

app = Flask(__name__)
api = Api(app)

# # Configuración de la base de datos PostgreSQL
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1111@localhost/autores_db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)


# # Crear la base de datos y la tabla si no existen
# with app.app_context():
#     db.create_all()


# Agregar recursos a la API
api.add_resource(AutorListResource, "/autores")
api.add_resource(AutorResource, "/autor/<int:autor_id>")

if __name__ == "__main__":
    app.run(debug=True)

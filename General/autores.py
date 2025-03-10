from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# Configuración de la base de datos PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1111@localhost/autores_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo de la tabla Autores
class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cargo = db.Column(db.Text, nullable=False)  # "¿Qué hace o su cargo?"

# Definir recursos RESTful
class AutorResource(Resource):
    def get(self, autor_id):
        autor = Autor.query.get(autor_id)
        if autor:
            return {"id": autor.id, "name": autor.name, "email": autor.email, "cargo": autor.cargo}, 200
        return {"message": "Autor no encontrado"}, 404

    def put(self, autor_id):
        autor = Autor.query.get(autor_id)
        if not autor:
            return {"message": "Autor no encontrado"}, 404

        data = request.get_json()
        autor.name = data.get("name", autor.name)
        autor.email = data.get("email", autor.email)
        autor.cargo = data.get("cargo", autor.cargo)

        db.session.commit()
        return {"message": "Autor actualizado", "id": autor.id}, 200

class AutorListResource(Resource):
    def get(self):
        autores = Autor.query.all()
        return [{"id": autor.id, "name": autor.name, "email": autor.email, "cargo": autor.cargo} for autor in autores], 200

    def post(self):
        data = request.get_json()
        new_autor = Autor(name=data["name"], email=data["email"], cargo=data["cargo"])
        db.session.add(new_autor)
        db.session.commit()
        return {"message": "Autor creado", "id": new_autor.id}, 201

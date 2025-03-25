from flask import request
from flask_restful import Resource
from ..Database.manager import DatabaseManager

db = DatabaseManager()

class Chatbot_Config(Resource):

    def get(self):
        try:
            query = "SELECT clave, valor, descripcion FROM configuraciones" #configuraciones 
            resultados = db.fetch_all(query)
            configs = [
                {"clave": clave, "valor": valor, "descripcion": descripcion}
                for clave, valor, descripcion in resultados
            ]
            return {"status": "fetched!", "configs": configs}, 200
        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}, 500

    def post(self):
        try:
            data = request.json
            clave = data.get("clave")
            valor = data.get("valor")
            descripcion = data.get("descripcion", "") #Recibe la configuración

            if not clave or not valor:
                raise RuntimeError("Faltan campos obligatorios: 'clave' y 'valor'.")

                    # Verifica si ya existe esa clave
            query_check = "SELECT 1 FROM configuraciones WHERE clave = ?"
            existente = db.fetch_all(query_check, (clave,))
            if existente:
                return {
                    "status": "failed!",
                    "reason": f"La clave '{clave}' ya existe. Usa PATCH para actualizarla."
                }, 409

            query = "INSERT INTO configuraciones (clave, valor, descripcion) VALUES (?, ?, ?)"
            db.execute_query(query, (clave, valor, descripcion))

            return {"status": "created!", "clave": clave}, 201
        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}, 500

    def patch(self):
        try:
            data = request.json
            clave = data.get("clave")
            nuevo_valor = data.get("valor")

            if not clave or nuevo_valor is None:
                raise RuntimeError("Se requiere 'clave' y nuevo 'valor'.")

            query = "UPDATE configuraciones SET valor = ? WHERE clave = ?"
            db.execute_query(query, (nuevo_valor, clave))

            return {"status": "updated!", "clave": clave, "nuevo_valor": nuevo_valor}, 200
        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}, 500

    def delete(self):
        try:
            data = request.json
            clave = data.get("clave")
            if not clave:
                raise RuntimeError("Se requiere la 'clave' a eliminar.")

            query = "DELETE FROM configuraciones WHERE clave = ?"
            db.execute_query(query, (clave,))
            return {"status": "deleted!", "clave": clave}, 200
        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}, 500

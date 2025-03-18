import os, sys
from flask import request
from flask_restful import Resource

from ..DataBase.manager import DatabaseManager

db = DatabaseManager()

# Definir recursos RESTful
class AutorResource(Resource):
    def get(self):
        try:
            # ===== Validacion de datos
            data = dict(request.json) if request.is_json else dict()
            
            # ===== Obtencion de valores
            table = data.get('name',None)
            if not(table): tables = ['rain','temperature','motion','pressure']
            else:          tables = [table,]

            # ===== Consulta BD
            result = {}
            for table in tables:
                fetch = db.fetch_all(f"SELECT * FROM {table};")
                result[table] = fetch                

            # ===== Confirmación
            return {"status":"fetched!","data":result}, 200
        
        # ===== Manejor de errores
        except KeyError as ex: return {"status":"failed!","reason":f"The key {ex} was not in request."}, 400

        except Exception as ex: return {"status":"failed!","reason":f"{ex}"}, 500

    def post(self):
        print(f"Se mando a llamar el codigo")
        return {'status':'failed!','cause':'Enpoint under construction... :('}, 503


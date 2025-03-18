import os, sys
from flask import request
from flask_restful import Resource

from ..Database.manager import DatabaseManager

db = DatabaseManager()


class Chatbot_Config(Resource):
    def get(self):
        try:
            
            # ===== Consulta BD
            configuraciones = {
                "config1":"val1",
                "config2":"val2",
                "config3":"val3"
            }

            # ===== Confirmación
            return {"status":"fetched!","configs":configuraciones}, 200
        
        # ===== Manejor de errores
        except KeyError as ex: return {"status":"failed!","reason":f"The key {ex} was not in request."}, 400

        except Exception as ex: return {"status":"failed!","reason":f"{ex}"}, 500
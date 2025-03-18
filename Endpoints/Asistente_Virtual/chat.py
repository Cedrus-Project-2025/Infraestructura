import os, sys
from flask import request
from flask_restful import Resource

from ..Database.manager import DatabaseManager

db = DatabaseManager()

class Chatbot_Response(Resource):

    def post(self):
        try:
            # ===== Validacion de datos
            data = request.json
            
            # ===== Obtencion de valores
            if type(data) in [dict]: pass
            else: raise RuntimeError("Se espera que el body del JSON sea un diccionario.")

            # ===== Consulta BD
            pregunta = data.get('pregunta',None)
            if pregunta == None: raise RuntimeError(f"No se encontró una pregunta valida, favor de corroborar.")

            # mando a llamar chatbot y ejecuto todo el proceso del chatbot

            respuesta = 'Esta es la respuesta a tu pregunta: ---'

            # ===== Confirmación
            return {"status":"created!","pregunta":pregunta,"respuesta":respuesta}, 201
        
        # ===== Manejor de errores
        except KeyError as ex: return {"status":"failed!","reason":f"The key {ex} was not in request."}, 400

        except Exception as ex: return {"status":"failed!","reason":f"{ex}"}, 500


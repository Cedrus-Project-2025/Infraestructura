import os, sys
import time
from flask import request
from flask_restful import Resource



class Chatbot_Response(Resource):
    def post(self):
        try:
            # ===== Validación de datos
            data = request.json
            if not isinstance(data, dict):
                raise RuntimeError("Se espera que el body del JSON sea un diccionario.")

            pregunta = data.get('pregunta', None)
            if not pregunta:
                raise RuntimeError("No se encontró una pregunta válida. Por favor, revisa tu solicitud.")

            # ===== Tiempo de inicio
            inicio = time.time()

            # ===== Simulación de respuesta del chatbot
            respuesta = f"Respuesta generada para: '{pregunta}'"
            # Aquí es donde llamarás a tu modelo real en el futuro

            # ===== Tiempo de fin y cálculo
            fin = time.time()
            tiempo_respuesta = round(fin - inicio, 3)  # tiempo en segundos con milisegundos

            # ===== Guardar en base de datos
            query = """
                INSERT INTO chatbot_interacciones (pregunta, respuesta, tiempo_respuesta) 
                VALUES (?, ?, ?)
            """
            db.execute_query(query, (pregunta, respuesta, tiempo_respuesta))

            # ===== Devolver respuesta
            return {
                "status": "created!",
                "pregunta": pregunta,
                "respuesta": respuesta,
                "tiempo_respuesta": tiempo_respuesta
            }, 201

        except KeyError as ex:
            return {"status": "failed!", "reason": f"The key {ex} was not in request."}, 400
        except Exception as ex:
            return {"status": "failed!", "reason": f"{ex}"}, 500
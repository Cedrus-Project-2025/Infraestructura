import os
import time
from flask import request
from flask_restful import Resource
from ..api_methods import API_Methods
from dotenv import load_dotenv

load_dotenv()



class ChatbotResponse(Resource):
    def __init__(self):
        url_db = os.getenv("URL_DATABASE", "")
        url_chatbot = os.getenv("URL_CHATBOT", "")

        self.api_base_datos = API_Methods(url=url_db)
        self.api_chat = API_Methods(url=url_chatbot)

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
            code, response = self.api_chat.POST(
                endpoint="/pregunta",
                data={"pregunta": pregunta}
            )

            # Verifica usando el atributo status_code del objeto Response
            if code.status_code != 200 or response.get("status") != "ok":
                return {
                    "status": "failed!",
                    "reason": "Respuesta inesperada del chatbot.",
                    "detalle": response
                }, 400

            respuesta = response.get("resultados", {}).get("respuesta")

            # ===== Tiempo de fin y cálculo
            fin = time.time()
            tiempo_respuesta = round(fin - inicio, 3)  # tiempo en segundos con milisegundos

            # ===== Guardar en base de datos
            code, response_db = self.api_base_datos.POST(
                endpoint="/chat/registers",
                data={
                    "nombre_tabla": "chatbot_interacciones",
                    "registros": [
                        {
                            "pregunta": pregunta,
                            "respuesta": respuesta,
                            "tiempo_respuesta": tiempo_respuesta
                        }
                    ]
                }
            )
            if code == "Failure to post":
                return {"error": "Error al guardar la interacción en la base de datos"}, 500

            # ===== Devolver respuesta
            return {
                "status": "created!",
                "pregunta": pregunta,
                "respuesta": respuesta,
                "tiempo_respuesta": tiempo_respuesta
            }, 201

        except Exception as ex:
            return {"status": "failed!", "reason": f"{ex}"}, 500
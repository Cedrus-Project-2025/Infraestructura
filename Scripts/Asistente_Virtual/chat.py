import os, time
import requests
from flask import Flask, request
from flask_restful import Api, Resource
from ..api_methods import API_Methods
from dotenv import load_dotenv

load_dotenv()

url_db = os.getenv("URL_DATABASE", "")

class Chatbot_Interacciones(Resource):
    def __init__(self):
        self.api_base_datos = API_Methods(url=url_db)
        #self.api_chat = API_Methods(link_chatbot)        

        #Obtener payload
    def post(self):
        try:
            ## Obtener el payload de la solicitud
            payload:dict = request.json
            pregunta = payload.get('pregunta')
            tiempo_inicio = time.time()
            if not pregunta:
                return {"error": "Falta el parámetro 'pregunta'"}, 400

            #Enviar pregunta a chat
            # code, response_chat = self.api_chat.POST(
            #     endpoint="/chat", #endpoint de Alan
            #     data={"pregunta": pregunta}
            # )
            # if code == "Failure to post":
            #     return {"error": "Error al enviar la pregunta al chatbot"}, 500
            # respuesta = response_chat.get("respuesta")
            # if not respuesta:
            #     return {"error": "No se recibió respuesta del chatbot"}, 500

            # Simulamos la respuesta del chatbot (hasta que tengas un endpoint real)
            respuesta = f"Respuesta simulada a: {pregunta}"
            tiempo_respuesta = time.time() - tiempo_inicio

            #Enviar pregunta y respuesta a la base de datos
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

            return {"pregunta": pregunta, "respuesta": respuesta}, 200

        except Exception as e:
            return {"error": str(e)}, 500

            
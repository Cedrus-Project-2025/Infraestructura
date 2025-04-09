import os
import requests
from flask import Flask, request
from flask_restful import Api, Resource
from ..api_methods import API_Methods
from dotenv import load_dotenv

load_dotenv()

url_db = os.getenv("URL_DATABASE", "")

def filtrar_campos(data, campos_a_excluir=("id", "fecha_creacion")):
    """
    Si 'data' es una lista de diccionarios, elimina de cada diccionario 
    las claves que aparecen en 'campos_a_excluir'.
    
    Si 'data' es un diccionario único, elimina esas claves directamente.
    """
    if isinstance(data, dict):
        return {k: v for k, v in data.items() if k not in campos_a_excluir}
    elif isinstance(data, list):
        return [
            {k: v for k, v in item.items() if k not in campos_a_excluir}
            for item in data
        ]
    else:
        return data

'endpoint: /chat/configs'
class Obtener_Configs(Resource):
    def __init__(self):
        self.api_base_datos = API_Methods(url=url_db)
        #self.api_chat = link_chatbot

    def get(self):

        ##consulta a la base de datos
        #Peticion para api_key
        code, response_key = self.api_base_datos.GET(
            endpoint="/chat/registers",
            data = {"nombre_tabla": "configuraciones"
            }
        )
        ''' response = {
            "status: "fetched!",
            "query": "SELECT FROM configuraciones",
            "result": [
                ("clave": "API_KEY", "valor": "123456789", "descripcion": "Clave de API"),
        }
        '''
        if code == "Failure to get data" or "result" not in response_key:
            return {"error": "Error al obtener la configuración"}, 500

        # Convertir la lista de registros en un diccionario
        configs = {item["clave"]: item["valor"] for item in response_key["result"]}

        # Función interna para construir el prompt 
        def build_prompt():

            prompt_introduccion = configs.get("PROMPT_INTRODUCCION", "")
            prompt_introduccion = prompt_introduccion.replace("{{insertar_name}}", configs.get("NAME", ""))#placeholders
            prompt_introduccion = prompt_introduccion.replace("{{insertar_project}}", configs.get("PROJECT", ""))
            prompt_introduccion = prompt_introduccion.replace("{{insertar_location}}", configs.get("LOCATION", ""))
            prompt_introduccion = prompt_introduccion.replace("{{insertar_experience}}", configs.get("EXPERIENCE", ""))
            prompt_introduccion = prompt_introduccion.replace("{{insertar_sector}}", configs.get("SECTOR", ""))


            prompt_personalidad = configs.get("PROMPT_PERSONALIDAD", "")
            prompt_personalidad = prompt_personalidad.replace("{{insertar_phrase1}}", configs.get("PHRASE1", ""))
            prompt_personalidad = prompt_personalidad.replace("{{insertar_phrase2}}", configs.get("PHRASE2", ""))

            prompt_objetivos = configs.get("PROMPT_OBJETIVOS", "")

            prompt_lineamientos = configs.get("PROMPT_LINEAMIENTOS", "")
            prompt_lineamientos = prompt_lineamientos.replace("{{insertar_concise}}", configs.get("CONCISE", ""))
            prompt_lineamientos = prompt_lineamientos.replace("{{insertar_callaction}}", configs.get("CALLACTION", ""))
            prompt_lineamientos = prompt_lineamientos.replace("{{insertar_negation1}}", configs.get("NEGATION1", ""))
            prompt_lineamientos = prompt_lineamientos.replace("{{insertar_negation2}}", configs.get("NEGATION2", ""))

        
            prompt_resp_indicaciones = configs.get("PROMPT_RESPUESTA_INDICACIONES", "")
            prompt_resp_indicaciones = prompt_resp_indicaciones.replace("{{insertar_name}}", configs.get("NAME", ""))
            prompt_resp_indicaciones = prompt_resp_indicaciones.replace("{{insertar_project}}", configs.get("PROJECT", ""))

            # Unificamos todas las secciones del prompt
            prompt_final = "\n\n".join([
                prompt_introduccion,
                prompt_personalidad,
                prompt_objetivos,
                prompt_lineamientos,
                prompt_resp_indicaciones
            ])
            return prompt_final

        # ----- Parte 2: Obtener la tabla de contexto -----

        #Peticion tablas para contexto
        code, response_proyectos = self.api_base_datos.GET(
            endpoint="/web/registers",
            data = {"nombre_tabla": "proyectos"}
        )
        ''' response_proyecto = {
                    "status: "fetched!",
                    "query": "SELECT FROM proyectos",
                    "result": [
                        ("título": "vhgvg", "descripcion": "erfer", "icono": "vdfvdf", "imagen": "vdfcvdf", "alt_text": "vdrg", "orden": "vdfvsdf"),
        '''
        if code == "Failure to get data" or "result" not in response_proyectos:
            proyectos = []
        else:
            proyectos = filtrar_campos(response_proyectos["result"], ("id", "fecha_creacion"))

        # ------------------- Selección de respuesta según el parámetro "modo" -------------------
        # Leer el parámetro "modo" desde la query string
        modo = request.args.get("modo")
        if modo == "apikey":
            if "API_KEY" not in configs:
                return {"error": "No se encontró la API_KEY"}, 404
            return {"api_key": configs["API_KEY"]}, 200
        elif modo == "prompt":
            return {"prompt": build_prompt()}, 200
        elif modo == "proyectos":
            return {"proyectos": proyectos}, 200
        else:
            # Si no se especifica "modo", se devuelven ambos: API_KEY, prompt y la tabla de amenidades
            result_data = {}
            if "API_KEY" in configs:
                result_data["api_key"] = configs["API_KEY"]
            result_data["prompt"] = build_prompt()
            result_data["proyectos"] = proyectos
            return result_data, 200































''''
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

'''
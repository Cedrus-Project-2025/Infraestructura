from flask import request
from flask_restful import Resource
import pandas as pd
import time
import os
import traceback
import re
from sqlalchemy import create_engine
from dotenv import load_dotenv
from ..api_methods import API_Methods

# Cargar las variables del archivo .env
load_dotenv()

API_URL = os.getenv("API_BASE_URL")

class Publicaciones(Resource):
    def __init__(self):
        self.api = API_Methods(url=API_URL)
        self.allowed_fields = [
            "post_id", "page_id", "page_name", "title", "description", "duration_sec",
            "publish_time", "caption_type", "permalink", "is_crosspost", "is_share",
            "post_type", "languages", "custom_labels", "funded_content_status", "data_comment", "date",
            "views", "reach", "reactions_comments_shares", "reactions", "comments", "shares",
            "total_clicks", "other_clicks", "link_clicks", "matc_pc", "seconds_viewed", "average_seconds_viewed",
            "estimated_earnings_usd", "ad_cpm_usd", "ad_impressions"
        ]

    def get(self):
        """
        Método GET para obtener datos de la tabla publicaciones
        
        Parámetros opcionales:
        - id: Filtrar por id específico
        - post_id: Filtrar por post_id
        - page_id: Filtrar por page_id
        - post_type: Filtrar por tipo de publicación
        - date_from: Filtrar desde una fecha (formato YYYY-MM-DD)
        - date_to: Filtrar hasta una fecha (formato YYYY-MM-DD)
        - fields: Campos específicos a devolver (separados por comas)
        - limit: Límite de registros a devolver
        - offset: Número de registros a omitir
        - sort_by: Campo por el cual ordenar
        - sort_dir: Dirección de ordenamiento (asc/desc)
        
        Retorna:
        - JSON con los datos de publicaciones
        """
        try:
            # Construir endpoint para la solicitud
            endpoint = "/business/registers"
            
            # Obtener parámetros de la solicitud
            params = {}
            for key in request.args:
                params[key] = request.args.get(key)

            # Asegurar que siempre se mande el nombre de la tabla
            params.setdefault('nombre_tabla', 'publicaciones')

            
            # Realizar solicitud GET a la API
            print(f"Parámetros enviados a la API externa: {params}")
            response, data = self.api.GET(endpoint, data=params)
            
            # Verificar si la respuesta es exitosa
            if response == "Failure to get data":
                return {
                    "status": "error",
                    "message": f"Error al obtener datos de publicaciones: {str(data)}",
                    "trace": traceback.format_exc()
                }, 500
            
            # Verificar si la respuesta es un objeto Response válido
            if not hasattr(response, 'status_code'):
                return {
                    "status": "error",
                    "message": "Respuesta inválida del servidor",
                    "trace": "No se recibió un objeto Response válido"
                }, 500
            
            # Formatear la respuesta
            return {
                "status": "success",
                "data": data,
                "message": "Datos de publicaciones obtenidos correctamente"
            }, response.status_code
            
        except Exception as e:
            error_msg = str(e)
            traceback_str = traceback.format_exc()
            
            return {
                "status": "error",
                "message": f"Error al obtener datos de publicaciones: {error_msg}",
                "trace": traceback_str
            }, 500


    def post(self):
        try:
            # Leer el cuerpo JSON de la solicitud
            data = request.get_json()

            nombre_tabla = data.get('nombre_tabla')
            registros = data.get('registros')

            if not nombre_tabla or not registros:
                return {"error": "Faltan 'nombre_tabla' o 'registros'."}, 400

            # Crear un DataFrame desde los registros
            df = pd.DataFrame(registros)

            # Mapeo de columnas del Excel al nombre de base de datos
            mapeo_columnas = {
                "Post ID": "post_id",
                "Page ID": "page_id",
                "Page name": "page_name",
                "Title": "title",
                "Description": "description",
                "Duration (sec)": "duration_sec",
                "Publish time": "publish_time",
                "Caption type": "caption_type",
                "Permalink": "permalink",
                "Is crosspost": "is_crosspost",
                "Is share": "is_share",
                "Post type": "post_type",
                "Languages": "languages",
                "Custom labels": "custom_labels",
                "Funded content status": "funded_content_status",
                "Data comment": "data_comment",
                "Date": "date",
                "Views": "views",
                "Reach": "reach",
                "Reactions": "reactions",
                "Comments": "comments",
                "Shares": "shares",
                "Total clicks": "total_clicks",
                "Other Clicks": "other_clicks",
                "Link Clicks": "link_clicks",
                "Matched Audience Targeting Consumption (Photo Click)": "matc_pc",
                "Seconds viewed": "seconds_viewed",
                "Average Seconds viewed": "average_seconds_viewed",
                "Estimated earnings (USD)": "estimated_earnings_usd",
                "Ad CPM (USD)": "ad_cpm_usd",
                "Ad impressions": "ad_impressions"
            }

            # Aplicar el mapeo solo si alguna columna del mapeo existe en el DataFrame
            columnas_presentes = [col for col in mapeo_columnas.keys() if col in df.columns]
            if columnas_presentes:
                df.rename(columns={col: mapeo_columnas[col] for col in columnas_presentes}, inplace=True)

            # Filtrar para dejar solo columnas válidas (por si trae columnas basura)
            columnas_validas = list(mapeo_columnas.values())
            df = df[[col for col in columnas_validas if col in df.columns]]

            # Crear conexión a la base de datos
            engine = create_engine(API_URL)

            # Insertar los datos
            df.to_sql(nombre_tabla, con=engine, if_exists='append', index=False)

            return {"message": "Datos insertados exitosamente en la base de datos"}, 200

        except Exception as e:
            return {"error": str(e)}, 500



    def delete(self):
        """
        Método DELETE para eliminar publicaciones con condiciones personalizadas.
        
        El cuerpo de la solicitud debe contener:
        {
            "nombre_tabla": "publicaciones",
            "condiciones": "WHERE reactions > 0"
        }
        """
        try:
            # Obtener los datos del cuerpo de la solicitud
            body_data = request.get_json()

            # Verificar que 'condiciones' esté presente
            if not body_data.get('condiciones'):
                return {"status": "error", "message": "'condiciones' es un parámetro obligatorio"}, 400

            # Configurar el endpoint
            endpoint = "/business/registers"

            # Enviar solicitud DELETE a la API con los datos (nombre_tabla y condiciones)
            response, data_response = self.api.DELETE(endpoint=endpoint, data=body_data)

            # Verificar si la respuesta fue exitosa
            if response == "Failure to delete":
                return {"status": "error", "message": f"Error al eliminar la publicación: {data_response}"}, 500

            return {
                "status": "success",
                "message": "Publicaciones eliminadas correctamente",
                "data": data_response
            }, 200

        except Exception as e:
            error_msg = str(e)
            traceback_str = traceback.format_exc()
            return {
                "status": "error",
                "message": f"Error al eliminar publicaciones: {error_msg}",
                "trace": traceback_str
            }, 500

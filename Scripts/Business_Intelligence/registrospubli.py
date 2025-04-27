from flask import request
from flask_restful import Resource
import pandas as pd
import time
import os
import traceback
import re
from dotenv import load_dotenv
from sqlalchemy import create_engine
from ..api_methods import API_Methods

# Cargar las variables del archivo .env
load_dotenv()

API_URL = os.getenv("API_BASE_URL")

class Publicaciones(Resource):
    def __init__(self):
        self.api = API_Methods(url=API_URL)

    def get(self):
        try:
            # Leer parámetros de la URL
            columnas = request.args.get("columnas")
            condicion = request.args.get("condicion")
            registros = request.args.get("registros", 10)  # Por defecto 10

            # Si no pasan columnas, ponemos columnas por default
            allowed_fields = [
                "id", "post_id", "page_id", "page_name", "title", "description", "duration_sec",
                "publish_time", "caption_type", "permalink", "is_crosspost", "is_share",
                "post_type", "languages", "custom_labels", "funded_content_status", "data_comment", "date",
                "views", "reach", "reactions_comments_shares", "reactions", "comments", "shares",
                "total_clicks", "other_clicks", "link_clicks", "matc_pc", "seconds_viewed", "average_seconds_viewed", 
                "estimated_earnings_usd", "ad_cpm_usd", "ad_impressions"
            ]

            columnas_list = columnas.split(",") if columnas else allowed_fields

            # Condiciones
            condiciones = [f"WHERE {condicion}"] if condicion else []

            # Armar payload para la API
            data = {
                "nombre_tabla": "publicaciones",
                "columnas": columnas_list,
                "condiciones": condiciones,
                "tipo_orden": {"id": "desc"},  # Ordenamos por ID descendente
                "registros": int(registros)
            }

            # Llamada a la API
            code, response = self.api.GET(
                endpoint="/business/registers",
                data=data
            )

            return response, code

        except Exception as e:
            return {"error": f"Error en el GET: {str(e)}"}, 500


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
        try:
            campo = request.args.get("campo")
            valor = request.args.get("valor")

            if not campo or not valor:
                return {"error": "Falta 'campo' o 'valor'"}, 400

            condiciones = f"WHERE {campo} = '{valor}'"

            data = {
                "nombre_tabla": "publicaciones",
                "condiciones": condiciones
            }

            code, response = self.api.DELETE(
                endpoint="/business/registers",
                data=data
            )

            return response, code

        except Exception as e:
            print(f"Error en el DELETE: {e}")
            print("Traceback completo:", traceback.format_exc())
            return {"error": f"Error en el DELETE: {str(e)}"}, 500
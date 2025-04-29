from flask import request
from flask_restful import Resource
import pandas as pd
import os
import traceback
from sqlalchemy import create_engine
from dotenv import load_dotenv
from ..api_methods import API_Methods

# Cargar variables de entorno
load_dotenv()
API_URL = os.getenv("API_BASE_URL")

class Audiencia(Resource):
    def __init__(self):
        self.api = API_Methods(url=API_URL)
        self.allowed_fields = [
            "fecha", "edad_promedio", "porcentaje_hombres",
            "porcentaje_mujeres", "ubicacion_principal"
        ]

    def get(self):
        """
        Método GET para obtener datos de la tabla audiencia
        
        Parámetros opcionales:
        - fecha: Filtrar por fecha exacta
        - edad_promedio: Filtrar por edad promedio (ej. >=30)
        - porcentaje_hombres: Filtrar por porcentaje de hombres
        - porcentaje_mujeres: Filtrar por porcentaje de mujeres
        - ubicacion_principal: Filtrar por ubicación principal

        Retorna:
        - JSON con los datos de audiencia
        """
        try:
            endpoint = "/business/registers"
            params = {key: request.args.get(key) for key in request.args}
            params.setdefault('nombre_tabla', 'audiencia')

            print(f"Parámetros enviados a la API externa: {params}")
            response, data = self.api.GET(endpoint, data=params)

            if response == "Failure to get data":
                return {
                    "status": "error",
                    "message": f"Error al obtener datos de audiencia: {str(data)}",
                    "trace": traceback.format_exc()
                }, 500

            if not hasattr(response, 'status_code'):
                return {
                    "status": "error",
                    "message": "Respuesta inválida del servidor",
                    "trace": "No se recibió un objeto Response válido"
                }, 500

            return {
                "status": "success",
                "data": data,
                "message": "Datos de audiencia obtenidos correctamente"
            }, response.status_code

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al obtener datos de audiencia: {str(e)}",
                "trace": traceback.format_exc()
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

            # Mapeo de columnas del Excel al nombre de base de datos para la tabla audiencia
            mapeo_columnas = {
                "Fecha": "fecha",
                "Edad Promedio": "edad_promedio",
                "Porcentaje Hombres (%)": "porcentaje_hombres",
                "Porcentaje Mujeres (%)": "porcentaje_mujeres",
                "Ubicación Principal": "ubicacion_principal"
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
        Método DELETE para eliminar registros de audiencia con condiciones personalizadas.

        Cuerpo de la solicitud:
        {
            "nombre_tabla": "audiencia",
            "condiciones": "WHERE edad_promedio > 30"
        }
        """
        try:
            body_data = request.get_json()

            if not body_data.get('condiciones'):
                return {"status": "error", "message": "'condiciones' es un parámetro obligatorio"}, 400

            endpoint = "/business/registers"
            response, data_response = self.api.DELETE(endpoint=endpoint, data=body_data)

            if response == "Failure to delete":
                return {"status": "error", "message": f"Error al eliminar audiencia: {data_response}"}, 500

            return {
                "status": "success",
                "message": "Registros de audiencia eliminados correctamente",
                "data": data_response
            }, 200

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al eliminar registros de audiencia: {str(e)}",
                "trace": traceback.format_exc()
            }, 500

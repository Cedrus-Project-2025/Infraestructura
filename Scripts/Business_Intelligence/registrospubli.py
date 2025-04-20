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
            payload = request.json if request.is_json else {}

            allowed_fields = [
                "id", "fecha", "alcance_total", "impresiones", "interacciones", "clics_en_enlace",
                "reacciones", "comentarios", "compartidos", "cpc_mxn", "tasa_de_conversion",
                "gasto_publicitario_mxn", "seguidores_nuevos", "total_de_seguidores"
            ]

            filters = []

            # Filtrado por ID (lista o entero)
            ids = payload.get("id")
            if ids is not None:
                if isinstance(ids, int):
                    ids = [ids]
                elif not isinstance(ids, list):
                    return {"error": "El campo 'id' debe ser un entero o una lista."}, 400
                filters.append(f"id IN ({','.join(map(str, ids))})")

            # Otros filtros
            for field, value in payload.items():
                if field == "id" or field not in allowed_fields:
                    continue

                if isinstance(value, (int, float)):
                    filters.append(f"{field} = {value}")
                elif isinstance(value, str):
                    match = re.match(r"^(<=|>=|=|<|>)(\d+(\.\d+)?)$", value)
                    if match:
                        operator, num_value, _ = match.groups()
                        filters.append(f"{field} {operator} {num_value}")
                    elif value.isdigit():
                        filters.append(f"{field} = {int(value)}")
                    else:
                        return {"error": f"Formato inválido para '{field}'. Usa operadores como >1000 o <=500."}, 400

            condiciones = f"WHERE {' AND '.join(filters)}" if filters else None

            data = {
                "nombre_tabla": "publicaciones",
                "columnas": allowed_fields,
                "condiciones": [condiciones] if condiciones else [],
                "tipo_orden": {"fecha": "desc"},
                "registros": 10
            }

            code, response = self.api.GET(
                endpoint="/business/registers",
                data=data
            )

            return response, code

        except Exception as e:
            return {"error": f"Error en el GET: {str(e)}"}, 500

    def post(self):
        try:
            # Verificar si el archivo está en la solicitud
            if 'file' in request.files:
                file = request.files['file']

                if file and file.filename.endswith('.xlsx'):
                    # Leer el archivo Excel con pandas
                    try:
                        df = pd.read_excel(file)
                    except Exception as e:
                        print(f"Error al leer el archivo Excel: {e}")
                        return {"error": f"Error al leer el archivo Excel: {e}"}, 500

                    # Procesar el archivo Excel (por ejemplo, convertir las filas en registros)
                    registros = []
                    for _, row in df.iterrows():
                        try:
                            registros.append({
                                "fecha": row["fecha"].strftime("%Y-%m-%d"),  # Formatear la fecha
                                "alcance_total": row["alcance_total"],
                                "impresiones": row["impresiones"],
                                "interacciones": row["interacciones"],
                                "clics_en_enlace": row["clics_en_enlace"],
                                "reacciones": row["reacciones"],
                                "comentarios": row["comentarios"],
                                "compartidos": row["compartidos"],
                                "cpc_mxn": row["cpc_mxn"],
                                "tasa_de_conversion": row["tasa_de_conversion"],
                                "gasto_publicitario_mxn": row["gasto_publicitario_mxn"],
                                "seguidores_nuevos": row["seguidores_nuevos"],
                                "total_de_seguidores": row["total_de_seguidores"]
                            })
                        except Exception as e:
                            print(f"Error procesando la fila {row}: {e}")
                            return {"error": f"Error procesando la fila {row}: {e}"}, 500

                    # Crear la conexión a la base de datos usando SQLAlchemy
                    engine = create_engine(API_URL)

                    # Insertar los registros en la base de datos
                    try:
                        df_to_insert = pd.DataFrame(registros)
                        df_to_insert.to_sql("publicaciones", con=engine, if_exists='append', index=False)
                        return {"message": "Datos insertados exitosamente en la base de datos"}, 200
                    except Exception as e:
                        print(f"Error al insertar los datos en la base de datos: {e}")
                        return {"error": f"Error al insertar los datos en la base de datos: {e}"}, 500

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

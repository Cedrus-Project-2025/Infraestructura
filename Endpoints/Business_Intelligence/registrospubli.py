from flask_restful import Resource, request
from api_methods import API_Methods
import time
import re
import os
from dotenv import load_dotenv

load_dotenv()  # Esto busca el archivo .env y carga las variables

API_URL = os.getenv("API_BASE_URL")

class PublicacionesAPI(Resource):
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
            return {"error": str(e)}, 500

    def post(self):
        try:
            payload = request.json

            campos_requeridos = [
                "fecha", "alcance_total", "impresiones", "interacciones",
                "clics_en_enlace", "reacciones", "comentarios", "compartidos",
                "cpc_mxn", "tasa_de_conversion", "gasto_publicitario_mxn",
                "seguidores_nuevos", "total_de_seguidores"
            ]

            # Verificar que los campos requeridos estén en el payload
            if not all(campo in payload for campo in campos_requeridos):
                return {"error": "Faltan campos obligatorios"}, 400

            # Verifica que los campos contengan datos válidos
            if not isinstance(payload["alcance_total"], (int, float)):
                return {"error": "'alcance_total' debe ser un número válido"}, 400

            # Crear los datos para enviar
            data = {
                "nombre_tabla": "publicaciones",
                "registros": [
                    {
                        **payload,
                        "timestamp": time.time()
                    }
                ]
            }

            # Hacer el POST a la API
            code, response = self.api.POST(
                endpoint="/business/registers",
                data=data
            )

            return response, code

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
            return {"error": str(e)}, 500

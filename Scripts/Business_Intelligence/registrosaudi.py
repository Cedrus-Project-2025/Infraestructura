from flask_restful import Resource, request
import time
import re
import os
from dotenv import load_dotenv
from ..api_methods import API_Methods

load_dotenv()  # Esto busca el archivo .env y carga las variables

API_URL = os.getenv("API_BASE_URL")

class AudienciaAPI(Resource):
    def __init__(self):
        self.api = API_Methods(url=API_URL)

    def get(self):
        try:
            data = request.json if request.is_json else {}

            allowed_fields = [
                "id", "fecha", "edad_promedio", "porcentaje_hombres",
                "porcentaje_mujeres", "ubicacion_principal"
            ]

            condiciones = []
            tipo_orden = {}
            valores = []

            ids = data.get("id", None)
            if ids is not None:
                if isinstance(ids, int):
                    ids = [ids]
                elif not isinstance(ids, list):
                    return {"status": "failed", "reason": "El campo 'id' debe ser un entero o una lista."}, 400

                condiciones.append(f"id IN ({','.join(['?']*len(ids))})")
                valores.extend(ids)

            for field, value in data.items():
                if field == "id":
                    continue
                if field not in allowed_fields:
                    continue

                if isinstance(value, (int, float)):
                    condiciones.append(f"{field} = ?")
                    valores.append(value)
                elif isinstance(value, str):
                    match = re.match(r"^(<=|>=|=|<|>)(\d+(\.\d+)?)$", value)
                    if match:
                        operator, num_value, _ = match.groups()
                        condiciones.append(f"{field} {operator} ?")
                        valores.append(float(num_value))
                    elif value.isdigit():
                        condiciones.append(f"{field} = ?")
                        valores.append(int(value))
                    else:
                        condiciones.append(f"{field} = ?")
                        valores.append(value)

            where_clause = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""

            api_data = {
                "nombre_tabla": "audiencia",
                "columnas": allowed_fields,
                "condiciones": [where_clause] if where_clause else [],
                "tipo_orden": {"fecha": "desc"},
                "registros": data.get("registros", 10)
            }

            code, response = self.api.GET(
                endpoint="/business/registers",
                data=api_data
            )
            return response, code

        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        try:
            payload = request.json
            campos_requeridos = [
                "fecha", "edad_promedio", "porcentaje_hombres",
                "porcentaje_mujeres", "ubicacion_principal"
            ]

            if not all(campo in payload for campo in campos_requeridos):
                return {"error": "Faltan campos obligatorios"}, 400

            data = {
                "nombre_tabla": "audiencia",
                "registros": [
                    {
                        **payload,
                        "timestamp": time.time()
                    }
                ]
            }

            code, response = self.api.POST(
                endpoint="/business/registers",
                data=data
            )

            return response, code

        except Exception as e:
            return {"error": str(e)}, 500

    def delete(self):
        try:
            data = request.json if request.is_json else {}
            ids = data.get("id", None)

            if isinstance(ids, int):
                ids = [ids]
            elif ids is None or isinstance(ids, list):
                pass
            else:
                return {"error": "El campo 'id' debe ser un entero, una lista o null."}, 400

            if ids:
                condiciones = f"id IN ({','.join(map(str, ids))})"
            else:
                return {"error": "Se requiere al menos un ID para eliminar registros."}, 400

            data = {
                "nombre_tabla": "audiencia",
                "condiciones": f"WHERE {condiciones}"
            }

            code, response = self.api.DELETE(
                endpoint="/business/registers",
                data=data
            )

            return response, code

        except Exception as e:
            return {"error": str(e)}, 500

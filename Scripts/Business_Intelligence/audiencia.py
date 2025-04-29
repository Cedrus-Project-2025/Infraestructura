import os, sys
from flask import request
from flask_restful import Resource


class Audiencia(Resource):
    def get(self):
        try:
            data = request.json if request.is_json else {}
            ids = data.get('id', None)

            if isinstance(ids, int):
                ids = [ids]
            elif ids is None or isinstance(ids, list):
                pass
            else:
                raise RuntimeError("El campo 'id' debe ser un entero, una lista o null.")

            # Especificamos los campos a seleccionar
            query = """
                SELECT fecha, edad_promedio, porcentaje_hombres, porcentaje_mujeres, ubicacion_principal
                FROM audiencia
            """
            if ids:
                query += f" WHERE id IN ({','.join(['?']*len(ids))})"

            # result = db.fetch_all(query, ids if ids else ())

            return {"status": "fetched", "data": 'result'}, 200

        except Exception as ex:
            return {"status": "failed", "reason": str(ex)}, 500


    def post(self):
        try:
            data = request.json
            if not isinstance(data, (list, dict)):
                raise RuntimeError("El body del JSON debe ser una lista o un diccionario.")

            if isinstance(data, dict):
                data = [data]

            for item in data:
                required_fields = ["fecha", "edad_promedio", "porcentaje_hombres", "porcentaje_mujeres", "ubicacion_principal"]
                if not all(field in item for field in required_fields):
                    raise RuntimeError(f"Faltan campos obligatorios en la solicitud: {required_fields}")

                # db.execute_query(
                #     "INSERT INTO audiencia (fecha, edad_promedio, porcentaje_hombres, porcentaje_mujeres, ubicacion_principal) VALUES (?, ?, ?, ?, ?)",
                #     (item["fecha"], item["edad_promedio"], item["porcentaje_hombres"], item["porcentaje_mujeres"], item["ubicacion_principal"])
                # )

            return {"status": "created"}, 201

        except Exception as ex:
            return {"status": "failed", "reason": str(ex)}, 500

    def delete(self):
        try:
            data = request.json if request.is_json else {}
            ids = data.get("id", None)

            if isinstance(ids, int):
                ids = [ids]
            elif ids is None or isinstance(ids, list):
                pass
            else:
                raise RuntimeError("El campo 'id' debe ser un entero, una lista o null.")

            if ids:
                placeholders = ",".join(["?"] * len(ids))
                query = f"DELETE FROM audiencia WHERE id IN ({placeholders})"
                # db.execute_query(query, ids)

            return {"status": "deleted"}, 200

        except Exception as ex:
            return {"status": "failed", "reason": str(ex)}, 500

import os, sys
from flask import request
from flask_restful import Resource
from ..Database.manager import DatabaseManager

db = DatabaseManager()


class Publicaciones(Resource):
    def get(self):
        try:
            data = request.json if request.is_json else {}

            # Lista de columnas permitidas en la tabla
            allowed_fields = [
                "id", "fecha", "alcance_total", "impresiones", "interacciones", "clics_en_enlace",
                "reacciones", "comentarios", "compartidos", "cpc_mxn", "tasa_de_conversion",
                "gasto_publicitario_mxn", "seguidores_nuevos", "total_de_seguidores"
            ]

            filters = []
            values = []

            # Filtrado por ID (permite un solo ID o una lista de IDs)
            ids = data.get("id", None)
            if ids is not None:
                if isinstance(ids, int):
                    ids = [ids]
                elif not isinstance(ids, list):
                    return {"status": "failed", "reason": "El campo 'id' debe ser un entero o una lista."}, 400

                filters.append(f"id IN ({','.join(['?']*len(ids))})")
                values.extend(ids)

            # Construimos los filtros dinámicos según los parámetros recibidos
            for key, value in data.items():
                if key == "id":
                    continue  # Ya manejamos ID arriba

                if "__" in key:  
                    field, operator = key.split("__", 1)  # Divide la clave (ej. seguidores_nuevos__gte)
                    if field not in allowed_fields:
                        continue  # Ignorar campos no válidos
                    
                    if operator == "gte":  # Mayor o igual (>=)
                        filters.append(f"{field} >= ?")
                    elif operator == "lte":  # Menor o igual (<=)
                        filters.append(f"{field} <= ?")
                    elif operator == "gt":  # Mayor que (>)
                        filters.append(f"{field} > ?")
                    elif operator == "lt":  # Menor que (<)
                        filters.append(f"{field} < ?")
                    elif operator == "eq":  # Igual (=)
                        filters.append(f"{field} = ?")
                    else:
                        continue

                    values.append(value)  # Guardamos el valor

            # Si hay filtros, los agregamos a la consulta
            where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

            query = f"SELECT * FROM publicaciones {where_clause}"
            result = db.fetch_all(query, values)

            return {"status": "fetched", "data": result}, 200

        except Exception as ex:
            return {"status": "failed", "reason": str(ex)}, 500


    def post(self):
        try:
            data = request.json
            if not isinstance(data, (list, dict)):
                raise RuntimeError("El body del JSON debe ser una lista o un diccionario.")

            if isinstance(data, dict):
                data = [data]

            required_fields = ["fecha", "alcance_total", "impresiones", "interacciones", "clics_en_enlace",
                            "reacciones", "comentarios", "compartidos", "cpc_mxn", "tasa_de_conversion",
                            "gasto_publicitario_mxn", "seguidores_nuevos", "total_de_seguidores"]

            for item in data:
                if not all(field in item for field in required_fields):
                    raise RuntimeError(f"Faltan campos obligatorios en la solicitud: {required_fields}")

                db.execute_query(
                    "INSERT INTO publicaciones (fecha, alcance_total, impresiones, interacciones, clics_en_enlace, "
                    "reacciones, comentarios, compartidos, cpc_mxn, tasa_de_conversion, gasto_publicitario_mxn, "
                    "seguidores_nuevos, total_de_seguidores) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (item["fecha"], item["alcance_total"], item["impresiones"], item["interacciones"],
                    item["clics_en_enlace"], item["reacciones"], item["comentarios"], item["compartidos"],
                    item["cpc_mxn"], item["tasa_de_conversion"], item["gasto_publicitario_mxn"],
                    item["seguidores_nuevos"], item["total_de_seguidores"])
                )

            return {
                "status": "created",
                "publicaciones": data  # Devuelve los datos enviados en la respuesta
            }, 201

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
                query = f"DELETE FROM publicaciones WHERE id IN ({placeholders})"
                db.execute_query(query, ids)

            return {"status": "deleted"}, 200

        except Exception as ex:
            return {"status": "failed", "reason": str(ex)}, 500
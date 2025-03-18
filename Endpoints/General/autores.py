import os, sys
from flask import request
from flask_restful import Resource

from ..Database.manager import DatabaseManager

db = DatabaseManager()

# Definir recursos RESTful
class Usuarios(Resource):
    def get(self):
        try:
            # ===== Validacion de datos
            data = dict(request.json) if request.is_json else dict()
            
            # ===== Obtencion de valores
            ids = data.get('id',None)
            if type(ids) == int: ids = [ids,]
            elif (type(ids) == list) or (ids == None): pass
            else: raise RuntimeError("Se espera que el valor de 'id' sea de tipo lista, int, o null.")

            # ===== Consulta BD
            result = {}
            if ids:
                placeholders = ",".join(["?"] * len(ids))  # Genera "?, ?, ?" según la cantidad de IDs
                query = f"SELECT * FROM usuarios WHERE id IN ({placeholders})"
                fetch = db.fetch_all(query, ids)

                # Organizar los datos por ID
                for row in fetch:
                    result[row[1]] = row  # Asegura que `fetch_all` devuelve diccionarios

            # ===== Confirmación
            return {"status":"fetched!","data":result}, 200
        
        # ===== Manejor de errores
        except KeyError as ex: return {"status":"failed!","reason":f"The key {ex} was not in request."}, 400

        except Exception as ex: return {"status":"failed!","reason":f"{ex}"}, 500

    def post(self):
        try:
            # ===== Validacion de datos
            data = request.json
            
            # ===== Obtencion de valores
            if type(data) in [list,dict]: pass
            else: raise RuntimeError("Se espera que el body del JSON sea una lista o un diccionario.")

            # ===== Consulta BD
            if type(data) == list:
                for dictionary in data:
                    nombre = dictionary.get('nombre')
                    if not(nombre): raise RuntimeError(f"Se espera que los diccionarios tengan la clave 'nombre'.")

                    correo = dictionary.get('correo')
                    if not(correo): raise RuntimeError(f"Se espera que los diccionarios tengan la clave 'correo'.")

                    contraseña = dictionary.get('contraseña')
                    if not(contraseña): raise RuntimeError(f"Se espera que los diccionarios tengan la clave 'contraseña'.")

                    db.execute_query("INSERT INTO usuarios(nombre, correo, contraseña) VALUES(?, ?, ?)",(nombre,correo,contraseña))

            # ===== Confirmación
            return {"status":"created!"}, 200
        
        # ===== Manejor de errores
        except KeyError as ex: return {"status":"failed!","reason":f"The key {ex} was not in request."}, 400

        except Exception as ex: return {"status":"failed!","reason":f"{ex}"}, 500

    def delete(self):
        try:
            # ===== Validacion de datos
            data = dict(request.json) if request.is_json else dict()
            
            # ===== Obtencion de valores
            ids = data.get('id',None)
            if type(ids) == int: ids = [ids,]
            elif (type(ids) == list) or (ids == None): pass
            else: raise RuntimeError("Se espera que el valor de 'id' sea de tipo lista, int, o null.")

            # ===== Consulta BD
            result = {}
            if ids:
                placeholders = ",".join(["?"] * len(ids))  # Genera "?, ?, ?" según la cantidad de IDs
                query = f"DELETE FROM usuarios WHERE id IN ({placeholders})"
                db.execute_query(query, ids)

            # ===== Confirmación
            return {"status":"deleted!"}, 200
        
        # ===== Manejor de errores
        except KeyError as ex: return {"status":"failed!","reason":f"The key {ex} was not in request."}, 400

        except Exception as ex: return {"status":"failed!","reason":f"{ex}"}, 500

    def patch(self):
        try:
            # ===== Validacion de datos
            data = dict(request.json) if request.is_json else dict()
            
            # ===== Obtencion de valores
            user_id = data.get("id", None)
            if not user_id: raise RuntimeError("El campo 'id' es obligatorio para actualizar un usuario.")

            actualizables = {"nombre", "correo", "contraseña"}
            datos_a_actualizar = {key:value for key,value in data.items() if key in actualizables}
            if not datos_a_actualizar: raise RuntimeError("No se proporcionaron campos válidos para actualizar.")

            # ===== Consulta BD
            set_clause = ", ".join([f"{key} = ?" for key in datos_a_actualizar.keys()])
            params = tuple(datos_a_actualizar.values()) + (user_id,)
            query = f"UPDATE usuarios SET {set_clause} WHERE id = ?"
            db.execute_query(query, params)

            # ===== Confirmación
            return {"status": "updated!", "updated_fields": list(datos_a_actualizar.keys())}, 200
        
        # ===== Manejor de errores
        except KeyError as ex: return {"status":"failed!","reason":f"The key {ex} was not in request."}, 400

        except Exception as ex: return {"status":"failed!","reason":f"{ex}"}, 500

from flask import request
from flask_restful import Resource
from ..Database.manager import DatabaseManager

db = DatabaseManager()

class ContactoCentro_Config(Resource):

    def get(self):
        try:
            query = "SELECT id_contacto_centro, nombre, telefono, horario_laboral_semana, horario_laboral_finde FROM CONTACTO_CENTRO"
            resultados = db.fetch_all(query)
            contactos = [
                {
                    "id_contacto_centro": id_contacto_centro,
                    "nombre": nombre,
                    "telefono": telefono,
                    "horario_laboral_semana": horario_laboral_semana,
                    "horario_laboral_finde": horario_laboral_finde
                }
                for id_contacto_centro, nombre, telefono, horario_laboral_semana, horario_laboral_finde in resultados
            ]
            return {"status": "fetched!", "contactos": contactos}, 200
        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}, 500

    def post(self):
        try:
            data = request.json
            nombre = data.get("nombre")
            telefono = data.get("telefono")
            horario_laboral_semana = data.get("horario_laboral_semana")
            horario_laboral_finde = data.get("horario_laboral_finde")

            if not nombre or not telefono or not horario_laboral_semana or not horario_laboral_finde:
                raise RuntimeError("Faltan campos obligatorios: 'nombre', 'telefono', 'horario_laboral_semana', y 'horario_laboral_finde'.")

            query = """
                INSERT INTO CONTACTO_CENTRO (nombre, telefono, horario_laboral_semana, horario_laboral_finde)
                VALUES (?, ?, ?, ?)
            """
            db.execute_query(query, (nombre, telefono, horario_laboral_semana, horario_laboral_finde))

            return {"status": "created!", "nombre": nombre}, 201
        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}, 500

    def patch(self):
        try:
            data = request.json
            id_contacto_centro = data.get("id_contacto_centro")
            nuevo_telefono = data.get("telefono")
            nuevo_horario_semana = data.get("horario_laboral_semana")
            nuevo_horario_finde = data.get("horario_laboral_finde")

            if not id_contacto_centro or not nuevo_telefono:
                raise RuntimeError("Se requiere 'id_contacto_centro' y 'telefono' para actualizar.")

            query = """
                UPDATE CONTACTO_CENTRO
                SET telefono = ?, horario_laboral_semana = ?, horario_laboral_finde = ?
                WHERE id_contacto_centro = ?
            """
            db.execute_query(query, (nuevo_telefono, nuevo_horario_semana, nuevo_horario_finde, id_contacto_centro))

            return {"status": "updated!", "id_contacto_centro": id_contacto_centro}, 200
        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}, 500

    def delete(self):
        try:
            data = request.json
            id_contacto_centro = data.get("id_contacto_centro")
            if not id_contacto_centro:
                raise RuntimeError("Se requiere 'id_contacto_centro' a eliminar.")

            query = "DELETE FROM CONTACTO_CENTRO WHERE id_contacto_centro = ?"
            db.execute_query(query, (id_contacto_centro,))
            return {"status": "deleted!", "id_contacto_centro": id_contacto_centro}, 200
        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}, 500

class OpcionesContacto_Config(Resource):

    def get(self):
        try:
            query = "SELECT id_opcion, tipo_contacto, icono, titulo, descripcion FROM OPCIONES_CONTACTO"
            resultados = db.fetch_all(query)
            opciones = [
                {
                    "id_opcion": id_opcion,
                    "tipo_contacto": tipo_contacto,
                    "icono": icono,
                    "titulo": titulo,
                    "descripcion": descripcion
                }
                for id_opcion, tipo_contacto, icono, titulo, descripcion in resultados
            ]
            return {"status": "fetched!", "opciones": opciones}, 200
        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}, 500

    def post(self):
        try:
            data = request.json
            tipo_contacto = data.get("tipo_contacto")
            icono = data.get("icono")
            titulo = data.get("titulo")
            descripcion = data.get("descripcion")

            if not tipo_contacto or not icono or not titulo or not descripcion:
                raise RuntimeError("Faltan campos obligatorios: 'tipo_contacto', 'icono', 'titulo', y 'descripcion'.")

            query = """
                INSERT INTO OPCIONES_CONTACTO (tipo_contacto, icono, titulo, descripcion)
                VALUES (?, ?, ?, ?)
            """
            db.execute_query(query, (tipo_contacto, icono, titulo, descripcion))

            return {"status": "created!", "tipo_contacto": tipo_contacto}, 201
        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}, 500

    def patch(self):
        try:
            data = request.json
            id_opcion = data.get("id_opcion")
            nuevo_tipo_contacto = data.get("tipo_contacto")
            nuevo_icono = data.get("icono")
            nuevo_titulo = data.get("titulo")
            nueva_descripcion = data.get("descripcion")

            if not id_opcion or not nuevo_tipo_contacto:
                raise RuntimeError("Se requiere 'id_opcion' y 'tipo_contacto' para actualizar.")

            query = """
                UPDATE OPCIONES_CONTACTO
                SET tipo_contacto = ?, icono = ?, titulo = ?, descripcion = ?
                WHERE id_opcion = ?
            """
            db.execute_query(query, (nuevo_tipo_contacto, nuevo_icono, nuevo_titulo, nueva_descripcion, id_opcion))

            return {"status": "updated!", "id_opcion": id_opcion}, 200
        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}, 500

    def delete(self):
        try:
            data = request.json
            id_opcion = data.get("id_opcion")
            if not id_opcion:
                raise RuntimeError("Se requiere 'id_opcion' a eliminar.")

            query = "DELETE FROM OPCIONES_CONTACTO WHERE id_opcion = ?"
            db.execute_query(query, (id_opcion,))
            return {"status": "deleted!", "id_opcion": id_opcion}, 200
        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}, 500

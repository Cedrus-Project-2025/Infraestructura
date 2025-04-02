from flask import request
from flask_restful import Resource
from ..Database.manager import DatabaseManager

db = DatabaseManager()

class TablaConsulta(Resource):
    def post(self):
        try:
            data = request.json
            tabla = data.get("tabla")
            if not tabla:
                raise RuntimeError("El campo 'tabla' es obligatorio.")

            # Lista de tablas permitidas (ajusta según las que hayas creado)
            tablas_validas = [
                "informacion_general",
                "ubicacion",
                "puntos_interes_cercanos",
                "terreno",
                "tamanos_lote",
                "restricciones_construccion",
                "amenidades",
                "modelos_casa",
                "caracteristicas",
                "plan_financiamiento_opciones",
                "beneficios",
                "requisitos",
                "plazos",
                "plan_financiamiento_condiciones",
                "contacto",
                "whatsapp",
                "redes_sociales",
                "faq",
                "testimonios",
                "etapas_desarrollo"
            ]

            if tabla not in tablas_validas:
                raise RuntimeError(f"La tabla '{tabla}' no está permitida.")

            # Realiza la consulta a la base de datos
            query = f"SELECT * FROM {tabla};"
            resultado = db.fetch_all(query)

            return {"status": "fetched!", "tabla": tabla, "datos": resultado}, 200

        except Exception as ex:
            return {"status": "failed!", "reason": str(ex)}, 500

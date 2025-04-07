from flask_restful import Resource, request
from api_methods import API_Methods

class AudienciaAPI(Resource):
    def __init__(self):
        self.api = API_Methods(url=" https://cedrus-database.onrender.com")

    def get(self):
        code, response = self.api.GET(
            endpoint="/business/audiencia"
        )
        return response, code

    def post(self):
        try:
            data = request.json
            campos_requeridos = [
                "fecha", "edad_promedio", "porcentaje_hombres",
                "porcentaje_mujeres", "ubicacion_principal"
            ]

            if not all(campo in data for campo in campos_requeridos):
                return {"error": "Faltan campos obligatorios"}, 400

            code, response = self.api.POST(
                endpoint="/business/audiencia",
                data=data
            )
            return response, code
        except Exception as e:
            return {"error": str(e)}, 500

    def delete(self):
        id_registro = request.args.get("id")
        if not id_registro:
            return {"error": "Falta el ID"}, 400

        code, response = self.api.DELETE(
            endpoint="/business/audiencia",
            data={"id": id_registro}
        )
        return response, code

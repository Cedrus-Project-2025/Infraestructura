import sys
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

# ===== Validaciones iniciales
load_dotenv()
sys.stdout = sys.stderr

# ===== Configuracion API
app = Flask(__name__)
CORS(app)
api = Api(app)


# ===== Endpoints Asistente Virtual
from Scripts.Asistente_Virtual.chat    import ChatbotResponse
from Scripts.Asistente_Virtual.configs import ObtenerConfigs

api.add_resource(ChatbotResponse, "/api/a/chat")
api.add_resource(ObtenerConfigs,  "/api/a/configs")




# ===== Endpoints BI
from Scripts.Business_Intelligence.registrospubli import PublicacionesAPI
from Scripts.Business_Intelligence.registrosaudi  import AudienciaAPI

api.add_resource(PublicacionesAPI, '/api/b/publicaciones')
api.add_resource(AudienciaAPI,     '/api/b/audiencia')




# ===== Endpoints Web
from Scripts.Desarrollo_Web.general import ObtenerConfigsGeneral

api.add_resource(ObtenerConfigsGeneral,     '/api/w/general')


if __name__ == '__main__':
    app.run(debug=True) 
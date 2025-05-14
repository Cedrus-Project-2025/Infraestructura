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
api = Api(app,prefix='/api')


# ===== Endpoints Asistente Virtual
from Scripts.Asistente_Virtual.chat    import ChatbotResponse
from Scripts.Asistente_Virtual.configs import ObtenerConfigs

api.add_resource(ChatbotResponse, "/a/chat")
api.add_resource(ObtenerConfigs,  "/a/configs")




# ===== Endpoints BI
from Scripts.Business_Intelligence.registrospubli import PublicacionesAPI
from Scripts.Business_Intelligence.registrosaudi  import AudienciaAPI

api.add_resource(PublicacionesAPI, '/b/publicaciones')
api.add_resource(AudienciaAPI,     '/b/audiencia')




# ===== Endpoints Web
from Scripts.Desarrollo_Web.general import ObtenerConfigsGeneral
from Scripts.Desarrollo_Web.proyectos    import ObtenerConfigsProyectos

api.add_resource(ObtenerConfigsGeneral, '/w/general')
api.add_resource(ObtenerConfigsProyectos, '/w/proyectos')


if __name__ == '__main__':
    app.run(debug=True) 
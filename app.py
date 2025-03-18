import os, sys
from dotenv import load_dotenv
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS

from Endpoints.General.usuarios import Usuarios
from Endpoints.General.rclone import validar_rclone
from Endpoints.Asistente_Virtual.chat import Chatbot_Response
from Endpoints.Asistente_Virtual.configs import Chatbot_Config

# ===== Validaciones iniciales
load_dotenv()
sys.stdout = sys.stderr
validar_rclone()

# ===== Configuracion API
app = Flask(__name__)
CORS(app)
api = Api(app)


# ===== Endpoints
api.add_resource(Usuarios,         "/api/g/usuarios")
api.add_resource(Chatbot_Response, "/api/a/chat")
api.add_resource(Chatbot_Config, "/api/a/chat_config")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
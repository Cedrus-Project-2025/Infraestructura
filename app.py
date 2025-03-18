import os, sys
from dotenv import load_dotenv
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS

from Endpoints.General.autores import AutorResource
from Endpoints.General.rclone import validar_rclone
from Endpoints.DataBase.manager import DatabaseManager

# ===== Validaciones iniciales
load_dotenv()
sys.stdout = sys.stderr
validar_rclone()

# ===== Configuracion API
app = Flask(__name__)
CORS(app)
api = Api(app)


# ===== Endpoints
api.add_resource(AutorResource, "/api/autor")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
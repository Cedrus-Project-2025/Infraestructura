import os, json
from flask import request
from flask_restful import Resource
from ..api_methods import API_Methods
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()


# ─────────────────────────────
# utilidades
# ─────────────────────────────
def filtrar_campos(
    data,
    campos_a_excluir=(
        "id", "fecha_creacion", "fecha_modificacion", "es_visible",
        "fecha_inicio", "fecha_fin", "orden", "icono", "color", "imagen",
        "url", "es_activo", "proyecto_amenidades_id", "proyecto_footer_id",
        "proyecto_id", "imagen_alt", "version", "boton_link", "boton_texto",
        "proyecto_about_id", "map_id", "map_center", "map_zoom", "map_options",
        "tiles_url", "tiles_attribution", "marker_icon", "polygon",
        "zoom_control", "proyecto_mapa_id", "coords", "img", "link", "logo",
        "imagen_principal", "estado", "copyright", "slug", "alt",
        "enlace_titulo", "contacto_titulo", "horarios_titulo"
    ),
):
    if isinstance(data, dict):
        return {k: v for k, v in data.items() if k not in campos_a_excluir}
    if isinstance(data, list):
        return [{k: v for k, v in item.items() if k not in campos_a_excluir} for item in data]
    return data


def build_prompt(cfg: dict) -> str:
    pi = cfg.get("PROMPT_INTRODUCCION", "")\
         .replace("{{insertar_name}}", cfg.get("NAME", ""))\
         .replace("{{insertar_project}}", cfg.get("PROJECT", ""))\
         .replace("{{insertar_location}}", cfg.get("LOCATION", ""))\
         .replace("{{insertar_experience}}", cfg.get("EXPERIENCE", ""))\
         .replace("{{insertar_sector}}", cfg.get("SECTOR", ""))

    pp = cfg.get("PROMPT_PERSONALIDAD", "")\
         .replace("{{insertar_phrase1}}", cfg.get("PHRASE1", ""))\
         .replace("{{insertar_phrase2}}", cfg.get("PHRASE2", ""))

    po = cfg.get("PROMPT_OBJETIVOS", "")

    pl = cfg.get("PROMPT_LINEAMIENTOS", "")\
         .replace("{{insertar_concise}}", cfg.get("CONCISE", ""))\
         .replace("{{insertar_callaction}}", cfg.get("CALLACTION", ""))\
         .replace("{{insertar_negation1}}", cfg.get("NEGATION1", ""))\
         .replace("{{insertar_negation2}}", cfg.get("NEGATION2", ""))

    pri = cfg.get("PROMPT_RESPUESTA_INDICACIONES", "")\
          .replace("{{insertar_name}}", cfg.get("NAME", ""))\
          .replace("{{insertar_project}}", cfg.get("PROJECT", ""))

    return "\n\n".join([pi, pp, po, pl, pri])


class ObtenerConfigs(Resource):
    """
    /chat/configs  → GET, POST, PATCH, DELETE
    """

    def __init__(self):
        self.api_base_datos = API_Methods(url=os.getenv("URL_DATABASE", ""))

    # ---------- GET ----------
    def get(self):
        # configuraciones ------------------------------------------------------
        code, response_key = self.api_base_datos.GET(
            endpoint="/chat/registers",
            data={"nombre_tabla": "configuraciones"}
        )
        if code == "Failure to get data" or "result" not in response_key:
            return {"error": "Error al obtener configuraciones"}, 500

        configs = {r["clave"]: r["valor"] for r in response_key["result"]}

        # tablas de contexto ---------------------------------------------------
        tablas, nombres = [], [
            "proyectos", "proyectos_about", "proyectos_slides",
            "proyectos_valores", "proyectos_mapa", "proyectos_mapa_locations",
            "proyectos_amenidades", "proyectos_amenidad_items",
            "proyectos_footer", "proyectos_footer_contacto",
            "proyectos_footer_horarios"
        ]
        for nombre in nombres:
            code, response = self.api_base_datos.GET(
                endpoint="/web/registers",
                data={"nombre_tabla": nombre}
            )
            filas = filtrar_campos(response["result"]) \
                    if code != "Failure to get data" and "result" in response else []
            tablas.append({"nombre": nombre, "filas": filas})

        modo = request.args.get("modo")
        if modo == "apikey":
            return (
                {"error": "No se encontró la API_KEY"}, 404
                if "API_KEY" not in configs else
                {"api_key": configs["API_KEY"]}, 200
            )
        if modo == "prompt":
            return {"prompt": build_prompt(configs)}, 200
        if modo == "tablas":
            return {"tablas": tablas}, 200

        return {
            "api_key": configs.get("API_KEY"),
            "prompt":  build_prompt(configs),
            "tablas":  tablas
        }, 200

    def post(self):
        data = request.get_json(force=True) or {}
        registros = data.get("registros")
        if not registros:
            return {"error": "No se proporcionaron registros."}, 400
        if any(not r.get("clave") or not r.get("valor") for r in registros):
            return {"error": "Cada registro requiere 'clave' y 'valor'."}, 400

        code, response = self.api_base_datos.POST(
            endpoint="/chat/registers",
            data={
                "nombre_tabla": "configuraciones",
                "registros":   registros
            }
        )
        if code == "Failure to post":
            return {"status": "failed", "reason": str(response)}, 500
        return {"status": "created"}, 201

    # ---------- PATCH ----------
    def patch(self):
        data = request.get_json(force=True) or {}
        if not data.get("cambios") or not data.get("condiciones"):
            return {"error": "Se requieren 'cambios' y 'condiciones'."}, 400
        if not data["condiciones"].strip().lower().startswith("where"):
            return {"error": "Las condiciones deben iniciar con WHERE."}, 400

        code, response = self.api_base_datos.PATCH(
            endpoint="/chat/registers",
            data={
                "nombre_tabla": data.get("nombre_tabla", "configuraciones"),
                "cambios":      data["cambios"],
                "condiciones":  data["condiciones"]
            }
        )
        if code == "Failure to patch":
            return {"status": "failed", "reason": str(response)}, 500
        return {"status": "updated"}, 200

    # ---------- DELETE  ----------
    def delete(self):
        data = request.get_json(force=True) or {}
        condiciones = data.get("condiciones")

        if not condiciones or not condiciones.strip().lower().startswith("where"):
            return {"error": "Se requieren 'condiciones' que inicien con WHERE."}, 400

        code, response = self.api_base_datos.DELETE(
            endpoint="/chat/registers",
            data={
                "nombre_tabla": data.get("nombre_tabla", "configuraciones"),
                "condiciones":  condiciones
            }
        )

        if code == "Failure to delete" or code.status_code >= 400:
            current_app.logger.error(f"Remote DELETE error: {response}")
            return {"status": "failed", "reason": str(response)}, 500

        return {"status": "deleted"}, 200

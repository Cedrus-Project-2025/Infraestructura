import os
from flask import request
from flask_restful import Resource
from ..api_methods import API_Methods
from dotenv import load_dotenv

load_dotenv()


def filtrar_campos(
    data,
    campos_a_excluir=(
        "id",
        "fecha_creacion",
        "fecha_modificacion",
        "es_visible",
        "fecha_inicio",
        "fecha_fin",
        "orden",
        "icono",
        "color",
        "imagen",
        "url",
        "es_activo",
        "proyecto_amenidades_id",
        "proyecto_footer_id",
        "proyecto_id",
        "imagen_alt",
        "version",
        "boton_link",
        "boton_texto",
        "proyecto_about_id",
        "map_id",
        "map_center",
        "map_zoom",
        "map_options",
        "tiles_url",
        "tiles_attribution",
        "marker_icon",
        "polygon",
        "zoom_control",
        "proyecto_mapa_id",
        "coords",
        "img",
        "link",
        "logo",
        "imagen_principal",
        "estado",
        "copyright",
        "slug",
        "alt",
        "enlace_titulo",
        "contacto_titulo",
        "horarios_titulo",
    ),
):
    """
    Si 'data' es una lista de diccionarios, elimina de cada diccionario 
    las claves que aparecen en 'campos_a_excluir'.
    
    Si 'data' es un diccionario único, elimina esas claves directamente.
    """
    if isinstance(data, dict):
        return {k: v for k, v in data.items() if k not in campos_a_excluir}
    elif isinstance(data, list):
        return [
            {k: v for k, v in item.items() if k not in campos_a_excluir}
            for item in data
        ]
    else:
        return data


def build_prompt(configs: dict) -> str:
    """
    Construye el prompt combinando las plantillas y placeholders.
    """
    # Introducción
    pi = configs.get("PROMPT_INTRODUCCION", "")
    pi = pi.replace("{{insertar_name}}", configs.get("NAME", ""))
    pi = pi.replace("{{insertar_project}}", configs.get("PROJECT", ""))
    pi = pi.replace("{{insertar_location}}", configs.get("LOCATION", ""))
    pi = pi.replace("{{insertar_experience}}", configs.get("EXPERIENCE", ""))
    pi = pi.replace("{{insertar_sector}}", configs.get("SECTOR", ""))

    # Personalidad
    pp = configs.get("PROMPT_PERSONALIDAD", "")
    pp = pp.replace("{{insertar_phrase1}}", configs.get("PHRASE1", ""))
    pp = pp.replace("{{insertar_phrase2}}", configs.get("PHRASE2", ""))

    # Objetivos
    po = configs.get("PROMPT_OBJETIVOS", "")

    # Lineamientos
    pl = configs.get("PROMPT_LINEAMIENTOS", "")
    pl = pl.replace("{{insertar_concise}}", configs.get("CONCISE", ""))
    pl = pl.replace("{{insertar_callaction}}", configs.get("CALLACTION", ""))
    pl = pl.replace("{{insertar_negation1}}", configs.get("NEGATION1", ""))
    pl = pl.replace("{{insertar_negation2}}", configs.get("NEGATION2", ""))

    # Respuesta/indicaciones
    pri = configs.get("PROMPT_RESPUESTA_INDICACIONES", "")
    pri = pri.replace("{{insertar_name}}", configs.get("NAME", ""))
    pri = pri.replace("{{insertar_project}}", configs.get("PROJECT", ""))

    # Unificamos todas las secciones
    return "\n\n".join([pi, pp, po, pl, pri])


class ObtenerConfigs(Resource):
    """
    Endpoint: GET /chat/configs
    Parámetros opcionales en query string:
      - modo=apikey   → devuelve {"api_key": "..."}
      - modo=prompt   → devuelve {"prompt": "..."}
      - modo=tablas   → devuelve {"tablas": [...]}
      - (por omisión) → devuelve api_key, prompt y tablas
    """

    def __init__(self):
        url_db = os.getenv("URL_DATABASE", "")
        self.api_base_datos = API_Methods(url=url_db)

    def get(self):
        # 1) Obtengo configuraciones
        code, response_key = self.api_base_datos.GET(
            endpoint="/chat/registers",
            data={"nombre_tabla": "configuraciones"},
        )
        if code == "Failure to get data" or "result" not in response_key:
            return {"error": "Error al obtener la configuración"}, 500

        configs = {item["clave"]: item["valor"] for item in response_key["result"]}

        # 2) Tablas de contexto
        nombres_tablas = [
            "proyectos",
            "proyectos_about",
            "proyectos_slides",
            "proyectos_valores",
            "proyectos_mapa",
            "proyectos_mapa_locations",
            "proyectos_amenidades",
            "proyectos_amenidad_items",
            "proyectos_footer",
            "proyectos_footer_contacto",
            "proyectos_footer_horarios",
        ]

        tablas = []
        for nombre in nombres_tablas:
            code, response = self.api_base_datos.GET(
                endpoint="/web/registers",
                data={"nombre_tabla": nombre},
            )
            if code != "Failure to get data" and "result" in response:
                filas = filtrar_campos(response["result"])
            else:
                filas = []
            tablas.append({"nombre": nombre, "filas": filas})

        # 3) Selección según modo
        modo = request.args.get("modo")
        if modo == "apikey":
            if "API_KEY" not in configs:
                return {"error": "No se encontró la API_KEY"}, 404
            return {"api_key": configs["API_KEY"]}, 200

        if modo == "prompt":
            return {"prompt": build_prompt(configs)}, 200

        if modo == "tablas":
            return {"tablas": tablas}, 200

        # 4) Respuesta por defecto: todo junto
        result = {}
        if "API_KEY" in configs:
            result["api_key"] = configs["API_KEY"]
        result["prompt"] = build_prompt(configs)
        result["tablas"] = tablas
        return result, 200

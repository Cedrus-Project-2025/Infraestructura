import os
from flask_restful import Resource
from ..api_methods import API_Methods
from dotenv import load_dotenv

load_dotenv()

class ObtenerConfigsGeneral(Resource):
    def __init__(self):
        self.api_base_datos = API_Methods(url=os.getenv("URL_DATABASE", ""))

    def get_field(self, data_list, field, default=''):
        return (data_list[0] or {}).get(field, default) if data_list else default

    def get(self):
        try:
            tablas = [
                ("home_slides_config", "main_home_slides_config"),
                ("home_slides", "main_home_slides"),
                ("about_config", "main_about_config"),
                ("about_stats", "main_about_stats"),
                ("services_config", "main_services_config"),
                ("services_items", "main_services_items"),
                ("testimonials_config", "main_testimonials_config"),
                ("testimonials_items", "main_testimonials_items"),
                ("contact_config", "main_contact_config"),
                ("contact_options", "main_contact_options"),
                ("contact_schedule", "main_contact_modals_schedule"),
                ("contact_branch", "main_contact_modals_advisor_sucursales"),
                ("contact_time", "main_contact_modals_advisor_horas"),
                ("map_config", "main_mapa_config"),
                ("map_markers", "main_mapa_marcadores"),
                ("footer_config", "main_footer_config"),
                ("footer_links", "main_footer_enlaces"),
                ("social_links", "main_social_links")
            ]

            data_respuestas = {}

            for key_name, table_name in tablas:
                code, response = self.api_base_datos.GET(
                    endpoint='/web/registers',
                    data={"nombre_tabla": table_name}
                )
                response_code = code.status_code if hasattr(code, "status_code") else code
                if response_code == 200 and response.get("status") == "fetched!":
                    data_respuestas[key_name] = response.get("result", [])
                else:
                    data_respuestas[key_name] = []

            # Construcción compacta de todos los datos organizados
            configuraciones = {
                "home_data": {
                    "titulo": self.get_field(data_respuestas['home_slides_config'], 'titulo_seccion'),
                    "subtitulo": self.get_field(data_respuestas['home_slides_config'], 'subtitulo_seccion'),
                    "slides": [{
                        "subtitulo": s.get('subtitulo', ''),
                        "titulo_parte1": s.get('titulo_parte1', ''),
                        "titulo_parte2": s.get('titulo_parte2', ''),
                        "boton_texto": s.get('boton_texto', ''),
                        "boton_link": s.get('boton_link', ''),
                        "imagen": s.get('imagen', ''),
                        "alt": s.get('alt', '')
                    } for s in data_respuestas['home_slides']]
                },
                "about_data": {
                    "subtitulo": self.get_field(data_respuestas['about_config'], 'subtitulo'),
                    "titulo_parte1": self.get_field(data_respuestas['about_config'], 'titulo_parte1'),
                    "titulo_parte2": self.get_field(data_respuestas['about_config'], 'titulo_parte2'),
                    "descripcion": self.get_field(data_respuestas['about_config'], 'descripcion'),
                    "imagen1": self.get_field(data_respuestas['about_config'], 'imagen1'),
                    "imagen2": self.get_field(data_respuestas['about_config'], 'imagen2'),
                    "stats": data_respuestas['about_stats']
                },
                "services_data": {
                    "subtitulo": self.get_field(data_respuestas['services_config'], 'subtitulo'),
                    "titulo_parte1": self.get_field(data_respuestas['services_config'], 'titulo_parte1'),
                    "titulo_parte2": self.get_field(data_respuestas['services_config'], 'titulo_parte2'),
                    "items": data_respuestas['services_items']
                },
                "testimonials_data": {
                    "subtitulo": self.get_field(data_respuestas['testimonials_config'], 'subtitulo'),
                    "titulo_parte1": self.get_field(data_respuestas['testimonials_config'], 'titulo_parte1'),
                    "titulo_parte2": self.get_field(data_respuestas['testimonials_config'], 'titulo_parte2'),
                    "testimonials": data_respuestas['testimonials_items']
                },
                "contact_center_data": {
                    "subtitulo": self.get_field(data_respuestas['contact_config'], 'subtitulo'),
                    "titulo_parte1": self.get_field(data_respuestas['contact_config'], 'titulo_parte1'),
                    "titulo_parte2": self.get_field(data_respuestas['contact_config'], 'titulo_parte2'),
                    "descripcion": self.get_field(data_respuestas['contact_config'], 'descripcion'),
                    "telefono": self.get_field(data_respuestas['contact_config'], 'telefono'),
                    "horario": self.get_field(data_respuestas['contact_config'], 'horario'),
                    "options": data_respuestas['contact_options'],
                    "schedule_options": data_respuestas['contact_schedule'],
                    "branch_options": data_respuestas['contact_branch'],
                    "time_options": data_respuestas['contact_time']
                },
                "mapa_data": {
                    "titulo": self.get_field(data_respuestas['map_config'], 'titulo'),
                    "subtitulo": self.get_field(data_respuestas['map_config'], 'subtitulo'),
                    "zoom_inicial": self.get_field(data_respuestas['map_config'], 'zoom_inicial', 5),
                    "latitud_central": self.get_field(data_respuestas['map_config'], 'latitud_central', 0),
                    "longitud_central": self.get_field(data_respuestas['map_config'], 'longitud_central', 0),
                    "markers": data_respuestas['map_markers']
                },
                "footer_data": {
                    "logo": self.get_field(data_respuestas['footer_config'], 'logo'),
                    "descripcion": self.get_field(data_respuestas['footer_config'], 'descripcion'),
                    "enlaces_titulo": self.get_field(data_respuestas['footer_config'], 'enlaces_titulo'),
                    "contacto_titulo": self.get_field(data_respuestas['footer_config'], 'contacto_titulo'),
                    "contacto_direccion": self.get_field(data_respuestas['footer_config'], 'contacto_direccion'),
                    "contacto_telefono": self.get_field(data_respuestas['footer_config'], 'contacto_telefono'),
                    "contacto_email": self.get_field(data_respuestas['footer_config'], 'contacto_email'),
                    "copyright": self.get_field(data_respuestas['footer_config'], 'copyright'),
                    "links": data_respuestas['footer_links']
                },
                "social_links": data_respuestas['social_links']
            }

            return {"status": "success", "message": "Configuraciones obtenidas correctamente", "data": configuraciones}, 200

        except Exception as e:
            return {"status": "error", "message": f"Error al obtener las configuraciones: {str(e)}", "data": None}, 500

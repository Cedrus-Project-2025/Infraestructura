import os
from flask_restful import Resource
from ..api_methods import API_Methods
from dotenv import load_dotenv

load_dotenv()

class ObtenerConfigsGeneral(Resource):
    def __init__(self):
        self.api_base_datos = API_Methods(url=os.getenv("URL_DATABASE", ""))

    def filtrar_campos(self, data_list):
        campos_excluir = {'id', 'activo', 'orden', 'icono', 'fecha_creacion', 'fecha_modificacion'}
        filtrados = []
        for item in data_list:
            nuevo_item = {k: v for k, v in item.items() if k not in campos_excluir}
            filtrados.append(nuevo_item)
        return filtrados

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
                    data_respuestas[key_name] = self.filtrar_campos(response.get("result", []))
                else:
                    data_respuestas[key_name] = []

            home_data = {
                'titulo': (data_respuestas['home_slides_config'][0] or {}).get('titulo_seccion', ''),
                'subtitulo': (data_respuestas['home_slides_config'][0] or {}).get('subtitulo_seccion', ''),
                'slides': [{
                    'subtitulo': s.get('subtitulo', ''),
                    'titulo_parte1': s.get('titulo_parte1', ''),
                    'titulo_parte2': s.get('titulo_parte2', ''),
                    'boton_texto': s.get('boton_texto', ''),
                    'boton_link': s.get('boton_link', ''),
                    'imagen': s.get('imagen', ''),
                    'alt': s.get('alt', '')
                } for s in data_respuestas['home_slides']]
            }

            about_data = {
                'subtitulo': (data_respuestas['about_config'][0] or {}).get('subtitulo', ''),
                'titulo_parte1': (data_respuestas['about_config'][0] or {}).get('titulo_parte1', ''),
                'titulo_parte2': (data_respuestas['about_config'][0] or {}).get('titulo_parte2', ''),
                'descripcion': (data_respuestas['about_config'][0] or {}).get('descripcion', ''),
                'imagen1': (data_respuestas['about_config'][0] or {}).get('imagen1', ''),
                'imagen2': (data_respuestas['about_config'][0] or {}).get('imagen2', ''),
                'stats': data_respuestas['about_stats']
            }

            services_data = {
                'subtitulo': (data_respuestas['services_config'][0] or {}).get('subtitulo', ''),
                'titulo_parte1': (data_respuestas['services_config'][0] or {}).get('titulo_parte1', ''),
                'titulo_parte2': (data_respuestas['services_config'][0] or {}).get('titulo_parte2', ''),
                'items': data_respuestas['services_items']
            }

            testimonials_data = {
                'subtitulo': (data_respuestas['testimonials_config'][0] or {}).get('subtitulo', ''),
                'titulo_parte1': (data_respuestas['testimonials_config'][0] or {}).get('titulo_parte1', ''),
                'titulo_parte2': (data_respuestas['testimonials_config'][0] or {}).get('titulo_parte2', ''),
                'testimonials': data_respuestas['testimonials_items']
            }

            contact_center_data = {
                'subtitulo': (data_respuestas['contact_config'][0] or {}).get('subtitulo', ''),
                'titulo_parte1': (data_respuestas['contact_config'][0] or {}).get('titulo_parte1', ''),
                'titulo_parte2': (data_respuestas['contact_config'][0] or {}).get('titulo_parte2', ''),
                'descripcion': (data_respuestas['contact_config'][0] or {}).get('descripcion', ''),
                'telefono': (data_respuestas['contact_config'][0] or {}).get('telefono', ''),
                'horario': (data_respuestas['contact_config'][0] or {}).get('horario', ''),
                'options': data_respuestas['contact_options'],
                'schedule_options': data_respuestas['contact_schedule'],
                'branch_options': data_respuestas['contact_branch'],
                'time_options': data_respuestas['contact_time']
            }

            mapa_data = {
                'titulo': (data_respuestas['map_config'][0] or {}).get('titulo', ''),
                'subtitulo': (data_respuestas['map_config'][0] or {}).get('subtitulo', ''),
                'zoom_inicial': (data_respuestas['map_config'][0] or {}).get('zoom_inicial', 5),
                'latitud_central': (data_respuestas['map_config'][0] or {}).get('latitud_central', 0),
                'longitud_central': (data_respuestas['map_config'][0] or {}).get('longitud_central', 0),
                'markers': data_respuestas['map_markers']
            }

            footer_data = {
                'logo': (data_respuestas['footer_config'][0] or {}).get('logo', ''),
                'descripcion': (data_respuestas['footer_config'][0] or {}).get('descripcion', ''),
                'enlaces_titulo': (data_respuestas['footer_config'][0] or {}).get('enlaces_titulo', ''),
                'contacto_titulo': (data_respuestas['footer_config'][0] or {}).get('contacto_titulo', ''),
                'contacto_direccion': (data_respuestas['footer_config'][0] or {}).get('contacto_direccion', ''),
                'contacto_telefono': (data_respuestas['footer_config'][0] or {}).get('contacto_telefono', ''),
                'contacto_email': (data_respuestas['footer_config'][0] or {}).get('contacto_email', ''),
                'copyright': (data_respuestas['footer_config'][0] or {}).get('copyright', ''),
                'links': data_respuestas['footer_links']
            }

            social_links = data_respuestas['social_links']

            return {
                "status": "success",
                "message": "Configuraciones obtenidas correctamente",
                "data": {
                    "home_data": home_data,
                    "about_data": about_data,
                    "services_data": services_data,
                    "testimonials_data": testimonials_data,
                    "contact_center_data": contact_center_data,
                    "mapa_data": mapa_data,
                    "footer_data": footer_data,
                    "social_links": social_links
                }
            }, 200

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al obtener las configuraciones: {str(e)}",
                "data": None
            }, 500
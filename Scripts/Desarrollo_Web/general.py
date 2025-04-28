import os
from flask_restful import Resource
from ..api_methods import API_Methods
from dotenv import load_dotenv

load_dotenv()

class ObtenerConfigsGeneral(Resource):
    def __init__(self):
        self.api_base_datos = API_Methods(url=os.getenv("URL_DATABASE", ""))

    def filtrar_campos(self, data_list):
        campos_excluir = {'id', 'activo', 'orden', 'fecha_creacion', 'fecha_modificacion','"icono"'}
        return [{k: v for k, v in item.items() if k not in campos_excluir} for item in data_list]

    def get_field(self, data_list, field, default=''):
        return (data_list[0] or {}).get(field, default) if data_list else default

    def get(self):
        try:
            tablas = {
                "home_slides_config": "main_home_slides_config",
                "home_slides": "main_home_slides",
                "about_config": "main_about_config",
                "about_stats": "main_about_stats",
                "services_config": "main_services_config",
                "services_items": "main_services_items",
                "testimonials_config": "main_testimonials_config",
                "testimonials_items": "main_testimonials_items",
                "contact_config": "main_contact_config",
                "contact_options": "main_contact_options",
                "contact_schedule": "main_contact_modals_schedule",
                "contact_branch": "main_contact_modals_advisor_sucursales",
                "contact_time": "main_contact_modals_advisor_horas",
                "map_config": "main_mapa_config",
                "map_markers": "main_mapa_marcadores",
                "footer_config": "main_footer_config",
                "footer_links": "main_footer_enlaces",
                "social_links": "main_social_links"
            }

            data_respuestas = {}

            for key_name, table_name in tablas.items():
                code, response = self.api_base_datos.GET(
                    endpoint='/web/registers',
                    data={"nombre_tabla": table_name}
                )
                response_code = code.status_code if hasattr(code, "status_code") else code
                if response_code == 200 and response.get("status") == "fetched!":
                    data_respuestas[key_name] = self.filtrar_campos(response.get("result", []))
                else:
                    data_respuestas[key_name] = []

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
                    } for s in data_respuestas['home_slides']],

                    "social_facebook": next((s['url'] for s in data_respuestas['social_links'] if s.get('tipo') == 'facebook'), ''),
                    "social_instagram": next((s['url'] for s in data_respuestas['social_links'] if s.get('tipo') == 'instagram'), ''),
                    "social_whatsapp": next((s['url'] for s in data_respuestas['social_links'] if s.get('tipo') == 'whatsapp'), '')

                },
                "about_data": {
                    "about_subtitulo": self.get_field(data_respuestas['about_config'], 'subtitulo'),
                    "about_titulo_parte1": self.get_field(data_respuestas['about_config'], 'titulo_parte1'),
                    "about_titulo_parte2": self.get_field(data_respuestas['about_config'], 'titulo_parte2'),
                    "about_descripcion": self.get_field(data_respuestas['about_config'], 'descripcion'),
                    "about_experiencia": next((item['cantidad'] for item in data_respuestas['about_stats'] if item['tipo'] == 'experiencia'), ''),
                    "about_experiencia_texto": next((item['texto'] for item in data_respuestas['about_stats'] if item['tipo'] == 'experiencia'), ''),
                    "about_proyectos": next((item['cantidad'] for item in data_respuestas['about_stats'] if item['tipo'] == 'proyectos'), ''),
                    "about_proyectos_texto": next((item['texto'] for item in data_respuestas['about_stats'] if item['tipo'] == 'proyectos'), ''),
                    "about_estados": next((item['cantidad'] for item in data_respuestas['about_stats'] if item['tipo'] == 'estados'), ''),
                    "about_estados_texto": next((item['texto'] for item in data_respuestas['about_stats'] if item['tipo'] == 'estados'), ''),
                    "about_imagen1": self.get_field(data_respuestas['about_config'], 'imagen1'),
                    "about_imagen2": self.get_field(data_respuestas['about_config'], 'imagen2')
                },
                "services_data": {
                    "services_subtitulo": self.get_field(data_respuestas['services_config'], 'subtitulo'),
                    "services_titulo_parte1": self.get_field(data_respuestas['services_config'], 'titulo_parte1'),
                    "services_titulo_parte2": self.get_field(data_respuestas['services_config'], 'titulo_parte2'),
                    "services_items": data_respuestas['services_items']
                },
                "testimonials_data": {
                    "testimonials_subtitulo": self.get_field(data_respuestas['testimonials_config'], 'subtitulo'),
                    "testimonials_titulo_parte1": self.get_field(data_respuestas['testimonials_config'], 'titulo_parte1'),
                    "testimonials_titulo_parte2": self.get_field(data_respuestas['testimonials_config'], 'titulo_parte2'),
                    "testimonios": data_respuestas['testimonials_items']
                },
                "contact_center_data": {
                    "contact_subtitulo": self.get_field(data_respuestas['contact_config'], 'subtitulo'),
                    "contact_titulo": self.get_field(data_respuestas['contact_config'], 'titulo_parte1'),
                    "opciones_contacto": [{
                        "icono": o.get('icono', ''),
                        "titulo": o.get('titulo', ''),
                        "descripcion": o.get('descripcion', ''),
                        "modal": o.get('modal', ''),
                        "aria_label": o.get('aria_label', '')
                    } for o in data_respuestas['contact_options']],
                    "telefono": self.get_field(data_respuestas['contact_config'], 'telefono'),
                    "horario": self.get_field(data_respuestas['contact_config'], 'horario'),
                    "modales": {
                        "schedule": {
                            "titulo": "Programa tu llamada",
                            "horarios": [{
                                "valor": h.get('valor', ''),
                                "texto": h.get('texto', '')
                            } for h in data_respuestas['contact_schedule']]
                        },
                        "data": {
                            "titulo": "Déjanos tus datos"
                        },
                        "advisor": {
                            "titulo": "Agenda una visita con un asesor",
                            "sucursales": [{
                                "valor": s.get('valor', ''),
                                "texto": s.get('texto', '')
                            } for s in data_respuestas['contact_branch']],
                            "horas": [{
                                "valor": t.get('valor', ''),
                                "texto": t.get('texto', '')
                            } for t in data_respuestas['contact_time']]
                        }
                    }
                },

                "mapa_data": {
                    "mapa_subtitulo": self.get_field(data_respuestas['map_config'], 'subtitulo'),
                    "mapa_titulo": self.get_field(data_respuestas['map_config'], 'titulo'),
                    "mapa_zoom_inicial": self.get_field(data_respuestas['map_config'], 'zoom_inicial', 5),
                    "mapa_centro_latitud": self.get_field(data_respuestas['map_config'], 'latitud_central', 0),
                    "mapa_centro_longitud": self.get_field(data_respuestas['map_config'], 'longitud_central', 0),
                    "marcadores": data_respuestas['map_markers']
                },
                "footer_data": {
                    # Columna principal
                    "footer_logo": self.get_field(data_respuestas['footer_config'], 'logo'),
                    "footer_descripcion": self.get_field(data_respuestas['footer_config'], 'descripcion'),

                    # Enlaces sociales
                    "footer_social_facebook": next((s['url'] for s in data_respuestas['social_links'] if s.get('tipo') == 'facebook'), ''),
                    "footer_social_instagram": next((s['url'] for s in data_respuestas['social_links'] if s.get('tipo') == 'instagram'), ''),
                    "footer_social_whatsapp": next((s['url'] for s in data_respuestas['social_links'] if s.get('tipo') == 'whatsapp'), ''),

                    # Enlaces rápidos
                    "footer_enlaces_titulo": self.get_field(data_respuestas['footer_config'], 'enlaces_titulo'),
                    "footer_link_inicio": next((l['url'] for l in data_respuestas['footer_links'] if l.get('texto') == 'Inicio'), ''),
                    "footer_link_nosotros": next((l['url'] for l in data_respuestas['footer_links'] if l.get('texto') == 'Nosotros'), ''),
                    "footer_link_servicios": next((l['url'] for l in data_respuestas['footer_links'] if l.get('texto') == 'Servicios'), ''),
                    "footer_link_contacto": next((l['url'] for l in data_respuestas['footer_links'] if l.get('texto') == 'Contacto'), ''),
                    "footer_link_proyectos": next((l['url'] for l in data_respuestas['footer_links'] if l.get('texto') == 'Proyectos'), ''),

                    # Sección de contacto
                    "footer_contacto_titulo": self.get_field(data_respuestas['footer_config'], 'contacto_titulo'),
                    "footer_contacto_direccion": self.get_field(data_respuestas['footer_config'], 'contacto_direccion'),
                    "footer_contacto_telefono": self.get_field(data_respuestas['footer_config'], 'contacto_telefono'),
                    "footer_contacto_email": self.get_field(data_respuestas['footer_config'], 'contacto_email'),

                    # Copyright
                    "footer_copyright": self.get_field(data_respuestas['footer_config'], 'copyright')
                }

            }

            return {"status": "success", "message": "Configuraciones obtenidas correctamente", "data": configuraciones}, 200

        except Exception as e:
            return {"status": "error", "message": f"Error al obtener las configuraciones: {str(e)}", "data": None}, 500

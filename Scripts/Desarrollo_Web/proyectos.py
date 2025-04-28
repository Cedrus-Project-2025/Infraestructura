import os
import json
from flask_restful import Resource
from ..api_methods import API_Methods
from dotenv import load_dotenv

load_dotenv()

class ObtenerConfigsProyectos(Resource):
    def __init__(self):
        self.api_base_datos = API_Methods(url=os.getenv("URL_DATABASE", ""))

    def get_field(self, data_list, field, default=''):
        return (data_list[0] or {}).get(field, default) if data_list else default

    def get(self):
        try:
            tablas = {
                "proyectos": "proyectos",
                "slides": "proyectos_slides",
                "about": "proyectos_about",
                "valores": "proyectos_valores",
                "mapa": "proyectos_mapa",
                "locations": "proyectos_mapa_locations",
                "amenidades": "proyectos_amenidades",
                "amenidad_items": "proyectos_amenidad_items",
                "diseno": "proyectos_diseno",
                "caracteristicas": "proyectos_diseno_caracteristicas",
                "materiales": "proyectos_diseno_materiales",
                "propuestas": "proyectos_diseno_propuestas",
                "estilos": "proyectos_diseno_estilos",
                "footer": "proyectos_footer",
                "footer_social": "proyectos_footer_social",
                "footer_links": "proyectos_footer_links",
                "footer_contacto": "proyectos_footer_contacto",
                "footer_horarios": "proyectos_footer_horarios"
            }

            data = {}

            for key, table in tablas.items():
                code, response = self.api_base_datos.GET(
                    endpoint='/web/registers',
                    data={"nombre_tabla": table}
                )
                response_code = code.status_code if hasattr(code, "status_code") else code
                if response_code == 200 and response.get("status") == "fetched!":
                    data[key] = response.get("result", [])
                else:
                    data[key] = []

            proyecto = data['proyectos'][0] if data['proyectos'] else {}
            mapa_info = data['mapa'][0] if data['mapa'] else {}
            diseno_info = data['diseno'][0] if data['diseno'] else {}
            amenidades_info = data['amenidades'][0] if data['amenidades'] else {}
            footer_info = data['footer'][0] if data['footer'] else {}

            respuesta = {
                "home_data": {
                    'titulo': proyecto.get('nombre', ''),
                    'subtitulo': proyecto.get('descripcion', ''),
                    'slides': [{
                        'subtitulo': s.get('subtitulo', ''),
                        'titulo_parte1': s.get('titulo_parte1', ''),
                        'titulo_parte2': s.get('titulo_parte2', ''),
                        'boton_texto': s.get('boton_texto', ''),
                        'boton_link': s.get('boton_link', ''),
                        'imagen': s.get('imagen', ''),
                        'alt': s.get('alt', '')
                    } for s in data['slides']]
                },
                "about_data": {
                    'titulo': self.get_field(data['about'], 'titulo'),
                    'subtitulo': self.get_field(data['about'], 'subtitulo'),
                    'descripcion': [self.get_field(data['about'], 'descripcion')],
                    'imagen': self.get_field(data['about'], 'imagen'),
                    'imagen_alt': self.get_field(data['about'], 'imagen_alt'),
                    'valores': [{
                        'icono': v.get('icono', ''),
                        'titulo': v.get('titulo', ''),
                        'descripcion': v.get('descripcion', '')
                    } for v in data['valores']]
                },
                "mapa_data": {}
            }

            if mapa_info:
                respuesta["mapa_data"] = {
                    'titulo': mapa_info.get('titulo', ''),
                    'descripcion': mapa_info.get('descripcion', ''),
                    'map_id': mapa_info.get('map_id', ''),
                    'map_center': list(map(float, mapa_info.get('map_center', '0,0').split(','))) if mapa_info.get('map_center') else [],
                    'map_zoom': mapa_info.get('map_zoom', 10),
                    'tiles_url': mapa_info.get('tiles_url', ''),
                    'tiles_attribution': mapa_info.get('tiles_attribution', ''),
                    'locations': [{
                        'name': l.get('name', ''),
                        'coords': list(map(float, l.get('coords', '0,0').split(','))) if l.get('coords') else [],
                        'img': l.get('img', ''),
                        'link': l.get('link', ''),
                        'description': l.get('description', '')
                    } for l in data['locations']]
                }
                if mapa_info.get('map_options'):
                    respuesta["mapa_data"]['map_options'] = json.loads(mapa_info['map_options'])

            respuesta["amenidades_data"] = {
                'titulo': amenidades_info.get('titulo', ''),
                'descripcion': amenidades_info.get('descripcion', ''),
                'amenidades': [{
                    'titulo': a.get('titulo', ''),
                    'descripcion': a.get('descripcion', ''),
                    'icono': a.get('icono', ''),
                    'imagen': a.get('imagen', ''),
                    'alt': a.get('alt', '')
                } for a in data['amenidad_items']]
            }

            respuesta["diseno_data"] = {
                'titulo': diseno_info.get('titulo', ''),
                'descripcion': diseno_info.get('descripcion', ''),
                'mapa_imagen': diseno_info.get('mapa_imagen', ''),
                'mapa_alt': diseno_info.get('mapa_alt', ''),
                'materiales_titulo': diseno_info.get('propuestas_titulo', ''),
                'materiales': [{
                    'nombre': m.get('nombre', ''),
                    'descripcion': m.get('descripcion', ''),
                    'icono': m.get('icono', '')
                } for m in data['materiales']],
                'propuestas_slides': [{
                    'imagen': p.get('imagen', ''),
                    'alt': p.get('alt', ''),
                    'caption': p.get('caption', '')
                } for p in data['propuestas']],
                'propuestas_estilos': [{
                    'nombre': e.get('nombre', ''),
                    'icono': e.get('icono', '')
                } for e in data['estilos']]
            }

            respuesta["footer_data"] = {
                'logo': footer_info.get('logo', ''),
                'descripcion': footer_info.get('descripcion', ''),
                'enlaces_titulo': footer_info.get('enlaces_titulo', ''),
                'contacto_titulo': footer_info.get('contacto_titulo', ''),
                'horarios_titulo': footer_info.get('horarios_titulo', ''),
                'copyright': footer_info.get('copyright', ''),
                'social_links': data['footer_social'],
                'links': data['footer_links'],
                'contacto_info': data['footer_contacto'],
                'horarios': data['footer_horarios']
            }

            return {
                "status": "success",
                "message": "Configuración de proyectos obtenida correctamente",
                "data": respuesta
            }, 200

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al obtener configuración de proyectos: {str(e)}",
                "data": None
            }, 500

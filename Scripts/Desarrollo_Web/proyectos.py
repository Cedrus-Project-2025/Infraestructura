import os
import json
from flask_restful import Resource
from ..api_methods import API_Methods
from dotenv import load_dotenv
from flask import request

load_dotenv()

class ObtenerConfigsProyectos(Resource):
    def __init__(self):
        self.api_base_datos = API_Methods(url=os.getenv("URL_DATABASE", ""))

    def get_field(self, data_list, field, default=''):
        return (data_list[0] or {}).get(field, default) if data_list else default

    def filtrar_campos(self, data_list):
        campos_excluir = {'id', 'activo', 'orden', 'fecha_creacion', 'fecha_modificacion'}
        return [{k: v for k, v in item.items() if k not in campos_excluir} for item in data_list]

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

                "contacto_config": "proyectos_contacto_config",
                "contacto_opciones": "proyectos_contacto_opciones",
                "contacto_modales": "proyectos_contacto_modal",
                "contacto_planes": "proyectos_contacto_planes",

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
                    data[key] = self.filtrar_campos(response.get("result", []))
                else:
                    data[key] = []

            # HOME
            proyecto = data['proyectos'][0] if data['proyectos'] else {}
            home_data_cumbres = {
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
                } for s in data['slides']],
                "social_facebook": next((s['url'] for s in data['footer_social'] if 'facebook' in (s.get('icono') or '').lower()), ''),
                "social_instagram": next((s['url'] for s in data['footer_social'] if 'instagram' in (s.get('icono') or '').lower()), ''),
                "social_whatsapp": next((s['url'] for s in data['footer_social'] if 'tiktok' in (s.get('icono') or '').lower()), ''),
            }

            # ABOUT
            about_info = data['about'][0] if data['about'] else {}
            about_data_cumbres = {
                'titulo': about_info.get('titulo', ''),
                'subtitulo': about_info.get('subtitulo', ''),
                'descripcion': [about_info.get('descripcion', '')],
                'imagen': about_info.get('imagen', ''),
                'imagen_alt': about_info.get('imagen_alt', ''),
                'valores_titulo': about_info.get('valores_titulo', ''),
                'valores': [{
                    'icono': v.get('icono', ''),
                    'titulo': v.get('titulo', ''),
                    'descripcion': v.get('descripcion', '')
                } for v in data['valores']],
                'conclusion': about_info.get('conclusion', ''),
            }

            # MAPA
            mapa_info = data['mapa'][0] if data['mapa'] else {}

            marker_icon = {
                'html': mapa_info.get('marker_icon_html', ''),
                'className': mapa_info.get('marker_icon_className', ''),
                'iconSize': json.loads(mapa_info.get('marker_icon_iconSize', '[30, 42]')),
                'iconAnchor': json.loads(mapa_info.get('marker_icon_iconAnchor', '[15, 42]')),
                'popupAnchor': json.loads(mapa_info.get('marker_icon_popupAnchor', '[0, -42]'))
            }

            mapa_data_cumbres = {
                'titulo': mapa_info.get('titulo', ''),
                'descripcion': mapa_info.get('descripcion', ''),
                'map_id': mapa_info.get('map_id', ''),
                'map_center': list(map(float, mapa_info.get('map_center', '0,0').split(','))) if mapa_info.get('map_center') else [],
                'map_zoom': mapa_info.get('map_zoom', 10),
                'tiles_url': mapa_info.get('tiles_url', ''),
                'tiles_attribution': mapa_info.get('tiles_attribution', ''),
                'locations': [
                    {
                        'name': l.get('name', ''),
                        'coords': list(map(float, l.get('coords', '0,0').split(','))) if l.get('coords') else [],
                        'img': l.get('img', ''),
                        'link': l.get('link', ''),
                        'description': l.get('description', '')
                    } for l in data['locations']
                ],
                'marker_icon': marker_icon,
                'polygon': json.loads(mapa_info.get('polygon', '[]')),
                'zoom_control': json.loads(mapa_info.get('zoom_control', '{}'))
            }

            if mapa_info.get('map_options'):
                mapa_data_cumbres['map_options'] = json.loads(mapa_info['map_options'])


            # AMENIDADES
            amenidades_info = data['amenidades'][0] if data['amenidades'] else {}
            amenidades_data_cumbres = {
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

            # DISEÑO
            diseno_info = data['diseno'][0] if data['diseno'] else {}
            diseno_personalizado_data_cumbres = {
                'titulo': diseno_info.get('titulo', ''),
                'descripcion': diseno_info.get('descripcion', ''),
                'mapa_imagen': diseno_info.get('mapa_imagen', ''),
                'mapa_alt': diseno_info.get('mapa_alt', ''),
                'caracteristicas': [{
                    'titulo': c.get('titulo', ''),
                    'descripcion': c.get('descripcion', ''),
                    'icono': c.get('icono', ''),
                    'imagen': c.get('imagen', ''),
                    'alt': c.get('alt', '')
                } for c in data['caracteristicas']],
                'materiales_titulo': diseno_info.get('materiales_titulo', ''),
                'materiales': [{
                    'nombre': mat.get('nombre', ''),
                    'descripcion': mat.get('descripcion', ''),
                    'icono': mat.get('icono', '')
                } for mat in data['materiales']],
                'propuestas_titulo': diseno_info.get('propuestas_titulo', ''),
                'propuestas_descripcion': diseno_info.get('propuestas_descripcion', ''),
                'propuestas_icono': diseno_info.get('propuestas_icono', ''),
                'propuestas_slides': [{
                    'imagen': prop.get('imagen', ''),
                    'alt': prop.get('alt', ''),
                    'caption': prop.get('caption', '')
                } for prop in data['propuestas']],
                'propuestas_estilos': [{
                    'nombre': est.get('nombre', ''),
                    'icono': est.get('icono', '')
                } for est in data['estilos']]
            }

            # CONTACTO
            contacto_info = data['contacto_config'][0] if data['contacto_config'] else {}
            contacto_opciones = data['contacto_opciones']
            contacto_modales = {m.get('id_opcion'): json.loads(m.get('contenido_modal', '{}')) for m in data['contacto_modales']}
            contacto_planes = [p for p in data['contacto_planes']]

            contacto_data_cumbres = {
                'titulo': contacto_info.get('titulo', ''),
                'descripcion': contacto_info.get('descripcion', ''),
                'opciones': []
            }

            for opcion in contacto_opciones:
                opcion_id = opcion.get('id_opcion')
                modal_info = contacto_modales.get(opcion_id, {})

                nueva_opcion = {
                    'id': opcion_id,
                    'icono': opcion.get('icono', ''),
                    'titulo': opcion.get('titulo', ''),
                    'descripcion': opcion.get('descripcion', ''),
                    'boton_texto': opcion.get('boton_texto', ''),
                    'modal': modal_info
                }

                if opcion_id == 'cumbres-financing':
                    nueva_opcion['modal']['planes'] = []
                    for plan in contacto_planes:
                        if plan.get('id_opcion') == opcion_id:
                            beneficios = json.loads(plan.get('beneficios', '[]'))
                            plan_info = {
                                'titulo': plan.get('titulo', ''),
                                'icono': plan.get('icono', ''),
                                'beneficios': beneficios
                            }
                            if plan.get('destacado'):
                                plan_info['destacado'] = True
                            if plan.get('tag'):
                                plan_info['tag'] = plan.get('tag')
                            nueva_opcion['modal']['planes'].append(plan_info)

                contacto_data_cumbres['opciones'].append(nueva_opcion)


            # FOOTER
            footer_info = data['footer'][0] if data['footer'] else {}

            footer_copyright = next(
                (f.get('copyright', '') for f in data['footer'] if f.get('tipo') == 'copyright'),
                ''
            )

            footer_terminos = [
                {'texto': f.get('texto', ''), 'url': f.get('url', '')}
                for f in data['footer']
                if f.get('tipo') == 'terminos'
            ]
            footer_data_cumbres = {
                'logo': footer_info.get('logo', ''),
                'descripcion': footer_info.get('descripcion', ''),

                'social_links': [{
                    'icono': s.get('icono', ''),
                    'url': s.get('url', '')
                } for s in data['footer_social']],

                'enlaces_titulo': footer_info.get('enlaces_titulo', ''),
                'enlaces': [{
                    'texto': l.get('texto', ''),
                    'url': l.get('url', '')
                } for l in data['footer_links']],

                # Información de contacto
                'contacto_titulo': footer_info.get('contacto_titulo', ''),
                'contacto_info': [{
                    'icono': c.get('icono', ''),
                    'texto': c.get('texto', ''),
                    'url': c.get('url', ''),
                    'target': c.get('target', '')
                } for c in data['footer_contacto']],

                'horarios_titulo': footer_info.get('horarios_titulo', ''),
                'horarios': [{
                    'dia': h.get('dia', ''),
                    'horas': h.get('horas', '')
                } for h in data['footer_horarios']],

                'copyright': footer_copyright,
                'terminos': footer_terminos
         

            }

            return {
                "status": "success",
                "message": "Configuración de proyectos obtenida correctamente",
                "data": {
                    "home_data_cumbres": home_data_cumbres,
                    "about_data_cumbres": about_data_cumbres,
                    "mapa_data_cumbres": mapa_data_cumbres,
                    "amenidades_data_cumbres": amenidades_data_cumbres,
                    "diseno_personalizado_data_cumbres": diseno_personalizado_data_cumbres,
                    "contacto_data_cumbres": contacto_data_cumbres,
                    "footer_data_cumbres": footer_data_cumbres
                }
            }, 200

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al obtener configuración de proyectos: {str(e)}",
                "data": None
            }, 500

    def post(self):
        try:
            data = request.get_json(force=True) or {}
            nombre_tabla = data.get("nombre_tabla")
            registros = data.get("registros")

            if not nombre_tabla or not registros:
                return {"error": "Se requieren 'nombre_tabla' y 'registros'."}, 400
            if any(not isinstance(r, dict) for r in registros):
                return {"error": "Cada registro debe ser un diccionario válido."}, 400

            code, response = self.api_base_datos.POST(
                endpoint="/web/registers",
                data={
                    "nombre_tabla": nombre_tabla,
                    "registros": registros
                }
            )

            if code == "Failure to post":
                return {"status": "failed", "reason": str(response)}, 500
            return {"status": "created"}, 201

        except Exception as e:
            print("ERROR EN POST:", traceback.format_exc())
            return {"error": "Error inesperado", "detalle": str(e)}, 500

    def patch(self):
        try:
            data = request.get_json(force=True) or {}
            nombre_tabla = data.get("nombre_tabla")
            cambios = data.get("cambios")
            condiciones = data.get("condiciones")

            if not nombre_tabla or not cambios or not condiciones:
                return {"error": "Se requieren 'nombre_tabla', 'cambios' y 'condiciones'."}, 400
            if not condiciones.strip().lower().startswith("where"):
                return {"error": "Las condiciones deben iniciar con WHERE."}, 400

            code, response = self.api_base_datos.PATCH(
                endpoint="/web/registers",
                data={
                    "nombre_tabla": nombre_tabla,
                    "cambios": cambios,
                    "condiciones": condiciones
                }
            )

            if code == "Failure to patch":
                return {"status": "failed", "reason": str(response)}, 500
            return {"status": "updated"}, 200

        except Exception as e:
            print("ERROR EN PATCH:", traceback.format_exc())
            return {"error": "Error inesperado", "detalle": str(e)}, 500

    def delete(self):
        try:
            data = request.get_json(force=True) or {}
            nombre_tabla = data.get("nombre_tabla")
            condiciones = data.get("condiciones")

            if not nombre_tabla or not condiciones:
                return {"error": "Se requieren 'nombre_tabla' y 'condiciones'."}, 400
            if not condiciones.strip().lower().startswith("where"):
                return {"error": "Las condiciones deben iniciar con WHERE."}, 400

            code, response = self.api_base_datos.DELETE(
                endpoint="/web/registers",
                data={
                    "nombre_tabla": nombre_tabla,
                    "condiciones": condiciones
                }
            )

            if code == "Failure to delete" or (hasattr(code, "status_code") and code.status_code >= 400):
                return {"status": "failed", "reason": str(response)}, 500
            return {"status": "deleted"}, 200

        except Exception as e:
            print("ERROR EN DELETE:", traceback.format_exc())
            return {"error": "Error inesperado", "detalle": str(e)}, 500
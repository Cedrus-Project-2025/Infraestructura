# Infraestructura (Branch: Damaris)

Este repositorio contiene la estructura y configuración necesaria para desplegar un entorno **Flask** con **Docker**, así como varios endpoints relacionados con configuraciones y un servicio de chatbot. La rama **Damaris** incluye desarrollos y cambios específicos a la infraestructura de este proyecto.

---

## Contenido del Repositorio

- **Files/**  
  (Carpeta de ejemplo o uso interno; revisa su contenido para más detalles)

- **Scripts/**  
  (Carpeta con scripts de endpoints, como el ChatbotResponse o el ObtenerConfigs)

- **.dockerignore**  
  Configuración para ignorar archivos y carpetas al construir la imagen Docker.

- **.gitignore**  
  Lista de archivos y carpetas que Git ignorará (por ejemplo, entornos virtuales, archivos de configuración locales, etc.).

- **README.md**  


- **app.py**  
  Archivo principal de Flask. Aquí se inicializa la aplicación y se definen rutas o recursos globales.

- **dockerfile**  
  Definición de la imagen Docker para el proyecto (basada en `python:3.11` u otra versión, según el repo).

- **requirements.txt**  
  Dependencias de Python necesarias para el proyecto (Flask, flask_restful, requests, etc.).

---

## Requisitos Previos

- **Python 3.11** (o la versión requerida en `dockerfile`) si deseas correr la aplicación de manera local.  
- **Docker** instalado, si deseas usar el contenedor.  
- **Git** para clonar o administrar este repositorio.

---

## Configuración Local (sin Docker)

Si prefieres ejecutar la aplicación localmente en tu máquina:

1. **Clona el repositorio** en la rama Damaris:
   ```bash
   git clone -b Damaris https://github.com/Cedrus-Project-2025/Infraestructura.git
   cd Infraestructura

## Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # en Linux/Mac
venv\Scripts\activate  # en Windows

## Instala las dependencias
pip install -r requirements.txt

## Configura las variables de entorno
URL_DATABASE=<URL_de_tu_base_de_datos>
URL_CHAT=<URL_de_tu_servicio_chatbot>

## Ejecuta la aplicación
python app.py

## Ejecución con Docker
## Crea y levanta el contenedor
clear; docker build -t cumbres-api .; docker run -p 5000:5000 cumbres-api #linux
cls; docker build -t cumbres-api .; docker run -p 5000:5000 cumbres-api #windows

## Endpoints Principales
1. Scripts/Asistente_Virtual/chat.py
2. Scripts/Asistente_Virtual/configs.py

## Notas Adicionales
- Docker:
Si encuentras problemas al construir o ejecutar la imagen, revisa los logs usando docker logs y asegúrate de que Docker esté actualizado.\
- Base de Datos y Servicios Externos:
Verifica que los endpoints /chat/registers y /web/registers estén activos y se puedan acceder desde tu entorno.


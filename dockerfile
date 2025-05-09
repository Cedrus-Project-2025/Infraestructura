# ========== Comando para crear y levantar docker
# clear; docker build -t cumbres-api .; docker run -p 502:502 cumbres-api
# ========== 

# Usa una imagen base de Python 3.11
FROM python:3.11

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos del proyecto a /app
COPY . /app

# Instalar las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 502
EXPOSE 502

# Comando para ejecutar la aplicación Flask usando Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:502", "app:app"]

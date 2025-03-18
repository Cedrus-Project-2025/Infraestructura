# ========== Comando para crear y levantar docker
# docker build -t cedrus-api .
# docker run -p 10000:10000 cedrus-api
# ========== 

# Usa una imagen base de Python 3.11
FROM python:3.11

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar rclone
RUN curl https://rclone.org/install.sh | bash

# Copiar los archivos del proyecto a /app
COPY . /app

# Instalar las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 10000
EXPOSE 10000

# Comando para ejecutar la aplicación Flask usando Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:10000", "app:app"]

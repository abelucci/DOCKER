# Usando una imagen de base de python para facilitarnos la creación de la imagen
FROM python:latest

# Creamos el directorio principal de trabajo
RUN mkdir /app
WORKDIR /app

# Copiamos nuestros archivos a nuestro directorio principal de trabajo
COPY . /app
COPY requirements.txt /app/

# Instalamos las dependencias de la aplicación
RUN pip install -r requirements.txt

# El puerto expuesto es el default de flask, el 5000 y también el puerto 8000 para Prometheus
EXPOSE 5000
EXPOSE 8000

# El comando ejecutado será nuestro script que arranca tanto Flask como Prometheus
CMD ["python", "app.py"]




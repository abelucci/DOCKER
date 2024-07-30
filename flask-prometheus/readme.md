# **CONSTRUIR DOCKER**

Creación de la imagen docker para poder utilizar metrics con prometheus.

* Construir imagen y probar su funcionamiento:

  ```
  docker push abelucci/phyton-flask-prometheus:1
  docker run -p 5000:5000 -p 8000:8000 abelucci/phyton-flask-prometheus:1
  ```
* Comprobar la imagen mediante los siguientes links:

  ```
  http://localhost:5000/
  http://localhost:8000/metrics
  ```

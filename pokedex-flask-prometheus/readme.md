# **CONSTRUIR DOCKER**

Creación de la imagen docker para poder utilizar metrics con prometheus.

* Construir imagen y probar su funcionamiento:

  ```
  docker build -t abelucci/pokedex-flask-prometheus:1 .
  docker run -p 5000:5000 -p 8000:8000 abelucci/pokedex-flask-prometheus:1
  docker push abelucci/pokedex-flask-prometheus:1
  ```
* Comprobar la imagen mediante los siguientes links:

  ```
  http://localhost:5000/
  http://localhost:8000/metrics
  ```

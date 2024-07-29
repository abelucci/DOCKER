# **COMPILAR**

Se encuentran todos los archivos para crear y personalizar el pokedex-flask.

Para poder personalizar la imagen, realizar lo siguiente:

* Compilar nuevamente el dockerfile:

  ```
  docker build -t abelucci/pokedex-flask-build:1 .
  ```
* Lanzar el contenedor:

  ```
  docker run --name pokedex-prometheus -p 5000:5000 abelucci/pokedex-flask-build:1
  ```

Funciona OK el docker file y los requirimientos, se puede utilizar de BASE para crear otras imagenes.

Opcionalmente, subir la imagen a Docker Hub.

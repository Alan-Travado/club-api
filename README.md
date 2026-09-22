# Sistema de Reservas - Club Deportivo Encuentro

API REST desarrollada en Python y Flask para la administracion de canchas, socios y reservas, con persistencia en MySQL.

## Integrantes

* Miembro 1: Arquitectura de BD y Persistencia
* Miembro 2: Motor de validacion de horarios
* Miembro 3: Modulo de canchas y deportes
* Miembro 4: Modulo de socios
* Miembro 5: Modulo de reservas
* Miembro 6: Estados, paginacion y hateoas
* Miembro 9: Testing, OpenAPI y documentacion

 ## Tecnologias utilizadas
 * Python 3.x
 * Flask
 * MySQL
 * Pytest (Testing)

 ## Instalacion y ejecucion 

1. Clonar el repositorio:
   '''bash
   git clone <LINK_DEL_REPOSITORIO>
   cd <NOMBRE_DEL PROYECTO>
2. Crear el entorno virtual:
   python3 -m venv venv
   source venv/bin/activate
3. Instalar las dependencias:
   pip install -r requirements.txt
4. Configurar la conexion a MySQL utilizado la configuracion del proyecto y ejecutar los scripts de creacion y carga inicial de la base de datos.
5: Ejecutar la aplicacion:
   python3 app.py

## Endpoints principales

1. Deportes 
   GET /deportes
2. Canchas
   GET /canchas
   POST /canchas
   GET /canchas{id}
   PATCH /canchas{id}
   DELETE /canchas{id}
   GET /canchas/disponibles
3. Socios
   GET /socios
   POST /socios
   GET /socios/{id}
   PATCH /socios/{id}
4. Reservas
   GET /reservas
   POST /reservas
   GET /reservas/{id}
   PUT /reservas/{id}/estado

## Paginacion
Los listados utilizan _limit y _offset.
* _limit: valor por defecto 10, entre 1 y 100.
* _offset: valor por defecto de 0 y mayor o igual a 0.
Los filtros se aplican antes de paginar y los resultados se ordenan por ID ascendente.

## Testing y OpenAPI
Las pruebas automatizadas se encuentran en:
   tests/
Para ejecutarlas:
   pytest
La especificacion de la API se encuentra en:
   swagger.yaml
Este archivo documenta los endpoints, parametros, solicitudes, respuestas y codigos HTTP de la API.

## Configuracion 
No se deben almacenar contraseñas ni otros secretos directamente en el repositorio.

La informacion de la aplicacion se persiste en MySQL y los deportes se caargan mediante el script de inicializacion de la base datos.

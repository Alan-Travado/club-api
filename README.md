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
* Docker y Docker Compose
* Pytest (testing)


 ## Instalacion y ejecucion 

## Instalación y ejecución (con Docker, recomendado)

Requiere tener Docker y Docker Compose instalados.

1. Clonar el repositorio:
```bash
   git clone <LINK_DEL_REPOSITORIO>
   cd club-api
   git checkout Develop
```
2. Crear el archivo de variables de entorno a partir de la plantilla:
```bash
   cp .env.example .env
```
   Completar `DB_PASSWORD` en `.env` con la contraseña acordada por el equipo.
3. Levantar todo (API + MySQL):
```bash
   docker compose up --build
```
4. Probar que responde: http://127.0.0.1:5000/deportes

Los scripts `init_db.sql` y `datos_prueba.sql` se ejecutan solos la primera vez que se crea la base, dentro del contenedor de MySQL.

Para frenar todo: `Ctrl + C`, o `docker compose down` para apagar los contenedores.

## Endpoints principales

## Endpoints

Deportes
* `GET /deportes`

Canchas
* `GET /canchas`
* `POST /canchas`
* `GET /canchas/{id}`
* `PATCH /canchas/{id}`
* `DELETE /canchas/{id}`
* `GET /canchas/disponibles`

Socios
* `GET /socios`
* `POST /socios`
* `GET /socios/{id}`
* `PATCH /socios/{id}`

Reservas
* `GET /reservas`
* `POST /reservas`
* `GET /reservas/{id}`
* `PUT /reservas/{id}/estado`

Extensiones opcionales
* `GET /bloqueos`
* `POST /bloqueos`
* `DELETE /bloqueos/{id}`
* `POST /reservas/recurrentes`

## Paginacion
Los listados utilizan _limit y _offset.
* _limit: valor por defecto 10, entre 1 y 100.
* _offset: valor por defecto de 0 y mayor o igual a 0.
Los filtros se aplican antes de paginar y los resultados se ordenan por ID ascendente.

## Testing

Las pruebas automatizadas están en la carpeta `tests/`. Para ejecutarlas (con el entorno virtual activado y las dependencias instaladas):

```bash
pytest
```
## Especificación de la API

El contrato completo (endpoints, parámetros, cuerpos de solicitud, respuestas y códigos HTTP) está documentado en `swagger.yaml`.


## Configuracion 
No se deben almacenar contraseñas ni otros secretos directamente en el repositorio.
La informacion de la aplicacion se persiste en MySQL y los deportes se caargan mediante el script de inicializacion de la base datos.
La contraseña real de la base va en `.env` (ignorado por Git); `.env.example` es la plantilla pública sin datos sensibles.
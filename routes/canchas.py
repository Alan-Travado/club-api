from flask import Blueprint, jsonify, request

from paginacion import armar_links
from services import canchas as service
from validators import canchas as validador
from validators.comunes import validar_sin_parametros

bp = Blueprint("canchas", __name__)


@bp.get("/canchas")
def listar_canchas():
    filtros, limit, offset = validador.validar_filtros_listado(request.args)
    canchas, total = service.listar_canchas(filtros, limit, offset)
    if total == 0:
        return "", 204
    respuesta = {
        "canchas": canchas,
        "_links": armar_links(limit, offset, total),
    }
    return jsonify(respuesta), 200

@bp.get("/canchas/disponibles")
def listar_canchas_disponibles():
    filtros, inicio, fin, limit, offset = validador.validar_disponibilidad(
        request.args
    )

    canchas, total = service.listar_canchas_disponibles(
        filtros,
        inicio,
        fin,
        limit,
        offset,
    )

    respuesta = {
        "canchas": canchas,
        "_links": armar_links(limit, offset, total),
    }

    return jsonify(respuesta), 200

@bp.post("/canchas")
def crear_cancha():
    validar_sin_parametros(request.args)
    body = request.get_json(silent=True)
    datos = validador.validar_creacion(body)
    nueva = service.crear_cancha(datos)
    return jsonify(nueva), 201


@bp.get("/canchas/<int:id_cancha>")
def obtener_cancha(id_cancha):
    validar_sin_parametros(request.args)
    return jsonify(service.obtener_cancha(id_cancha)), 200


@bp.patch("/canchas/<int:id_cancha>")
def actualizar_cancha(id_cancha):
    validar_sin_parametros(request.args)
    body = request.get_json(silent=True)
    datos = validador.validar_actualizacion(body)

    service.actualizar_cancha(id_cancha, datos)

    return "", 204


@bp.delete("/canchas/<int:id_cancha>")
def eliminar_cancha(id_cancha):
    validar_sin_parametros(request.args)
    service.eliminar_cancha(id_cancha)
    return "", 204

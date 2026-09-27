from flask import Blueprint, jsonify, request

from paginacion import armar_links
from services import socios as service
from validators import socios as validador
from validators.comunes import validar_sin_parametros

bp = Blueprint("socios", __name__)


@bp.get("/socios")
def listar_socios():
    filtros, limit, offset = validador.validar_filtros_listado(request.args)
    socios, total = service.listar_socios(filtros, limit, offset)
    if total == 0:
        return "", 204
    respuesta = {
        "socios": socios,
        "_links": armar_links(limit, offset, total),
    }
    return jsonify(respuesta), 200


@bp.post("/socios")
def crear_socio():
    validar_sin_parametros(request.args)
    body = request.get_json(silent=True)
    datos = validador.validar_creacion(body)
    nuevo = service.crear_socio(datos)
    return jsonify(nuevo), 201


@bp.get("/socios/<int:id_socio>")
def obtener_socio(id_socio):
    validar_sin_parametros(request.args)
    return jsonify(service.obtener_socio(id_socio)), 200


@bp.patch("/socios/<int:id_socio>")
def actualizar_socio(id_socio):
    validar_sin_parametros(request.args)
    body = request.get_json(silent=True)
    actual = service.obtener_socio(id_socio)
    datos = validador.validar_actualizacion(body, actual)
    service.actualizar_socio(id_socio, datos)
    return "", 204

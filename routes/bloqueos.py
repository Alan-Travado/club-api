from flask import Blueprint, jsonify,request

from paginacion import armar_links
from services import bloqueos as service
from validators import bloqueos as validador
from validators.comunes import validar_sin_parametros

bp = Blueprint("bloqueos", __name__)

@bp.get("/bloqueos")
def listar_bloqueos():
    filtros, limit, offset = validador.validar_filtros_listado(request.args)
    bloqueos, total = service.listar_bloqueos(filtros, limit, offset)
    if total == 0:
        return "", 204
    respuesta={
        "bloqueos" : bloqueos,
        "_links" : armar_links(limit, offset, total),
    }
    return jsonify(respuesta), 200

@bp.post("/bloqueos")
def crear_bloqueo():
    validar_sin_parametros(request.args)
    body = request.get_json(silent=True)
    datos = validador.validar_creacion(body)
    nuevo = service.crear_bloqueo(datos)
    return jsonify(nuevo), 201

@bp.delete("/bloqueos/<int:id_bloqueo>")
def eliminar_bloqueo(id_bloqueo):
    validar_sin_parametros(request.args)
    service.eliminar_bloqueo(id_bloqueo)
    return "", 204

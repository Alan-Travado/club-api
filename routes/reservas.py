from flask import Blueprint, jsonify, request

from errors import ApiError
from paginacion import armar_links
from services import reservas as service
from validators import reservas as validador

bp = Blueprint("reservas", __name__)


@bp.get("/reservas")
def listar_reservas():
    filtros, limit, offset = validador.validar_filtros_listado(request.args)
    reservas, total = service.listar_reservas(filtros, limit, offset)
    if total == 0:
        return "", 204
    return jsonify(
        {"reservas": reservas, "_links": armar_links(limit, offset, total)}
    ), 200

@bp.post("/reservas")
def crear_reserva():
    body = request.get_json(silent=True)
    datos = validador.validar_creacion(body)
    nueva = service.crear_reserva(datos)

    return jsonify(nueva), 201

@bp.get("/reservas/<int:id_reserva>")
def obtener_reserva(id_reserva):
    return jsonify(service.obtener_reserva(id_reserva)), 200

@bp.put("/reservas/<int:id_reserva>/estado")
def establecer_estado(id_reserva):
    validador.validar_id(id_reserva)
    if request.args:
        raise ApiError(
            400,
            "PARAMETRO_DESCONOCIDO",
            "Parámetro desconocido",
            "Este endpoint no admite parámetros de consulta",
        )
    estado = validador.validar_cambio_estado(request.get_json(silent=True))
    return jsonify(service.cambiar_estado(id_reserva, estado)), 200

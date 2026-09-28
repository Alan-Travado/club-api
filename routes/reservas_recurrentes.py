from flask import Blueprint, request, jsonify

from services import reservas_recurrentes as service
from validators import reservas_recurrentes as validador
from validators.comunes import validar_sin_parametros

bp = Blueprint("reservas_recurrentes", __name__)


def serializar_reserva(reserva):
    resultado = reserva.copy()

    if "fecha_hora_inicio" in resultado:
        resultado["fecha_hora_inicio"] = (
            reserva["fecha_hora_inicio"].isoformat(
                timespec="microseconds"
            )
        )

    if "fecha_hora_fin" in resultado:
        resultado["fecha_hora_fin"] = (
            reserva["fecha_hora_fin"].isoformat(
                timespec="microseconds"
            )
        )

    return resultado


@bp.post("/reservas/recurrentes")
def crear_reservas_recurrentes():
    validar_sin_parametros(request.args)
    body = request.get_json(silent=True)

    datos = validador.validar_creacion(body)

    reservas = service.crear_reservas_recurrentes(datos)

    reservas_serializadas = [
        serializar_reserva(reserva)
        for reserva in reservas
    ]

    return jsonify({
        "reservas": reservas_serializadas
    }), 201
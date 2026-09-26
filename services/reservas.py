from errors import ApiError
from repositories import reservas as repo
from services.estado_reserva import ahora_gmt3, resolver_transicion


def listar_reservas(filtros, limit, offset):
    return repo.listar(filtros, limit, offset)


def cambiar_estado(id_reserva, estado_nuevo, ahora=None):
    reserva = repo.obtener_por_id(id_reserva)
    if reserva is None:
        raise ApiError(
            404,
            "RESERVA_NO_ENCONTRADA",
            "Reserva no encontrada",
            f"No existe una reserva con id {id_reserva}",
        )
    if ahora is None:
        ahora = ahora_gmt3()
    estado_anterior = reserva["estado"]
    if resolver_transicion(
        estado_anterior,
        estado_nuevo,
        reserva["fecha_hora_inicio"],
        reserva["fecha_hora_fin"],
        ahora,
    ):
        actualizado = repo.actualizar_estado(id_reserva, estado_nuevo, estado_anterior)
        if not actualizado:
            raise ApiError(
                400,
                "TRANSICION_NO_PERMITIDA",
                "Transicion no permitida",
                "La reserva cambio de estado mientras se procesaba la solicitud",
            )
        reserva["estado"] = estado_nuevo
    return repo.formatear(reserva)

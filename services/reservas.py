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
    if resolver_transicion(
        reserva["estado"],
        estado_nuevo,
        reserva["fecha_hora_inicio"],
        reserva["fecha_hora_fin"],
        ahora,
    ):
        repo.actualizar_estado(id_reserva, estado_nuevo)
        reserva["estado"] = estado_nuevo
    return repo.formatear(reserva)

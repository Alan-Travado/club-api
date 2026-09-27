from datetime import datetime, timedelta, timezone

from errors import ApiError

GMT3 = timezone(timedelta(hours=-3))
ESTADOS = frozenset({"confirmada", "cancelada", "finalizada"})


def ahora_gmt3():
    """Hora de reloj en GMT-3, sin convertir desde otra zona."""
    return datetime.now(GMT3).replace(tzinfo=None)


def resolver_transicion(actual, nuevo, inicio, fin, ahora):
    """Devuelve True si hay que guardar el cambio. False si el estado se repite.

    confirmada -> cancelada solo si el inicio todavía no llegó.
    confirmada -> finalizada solo si ya se alcanzó el fin.
    cancelada y finalizada no pasan a otro estado.
    """
    if nuevo not in ESTADOS:
        raise ApiError(
            400,
            "CAMPO_INVALIDO",
            "Campo inválido",
            "El campo 'estado' debe ser confirmada, cancelada o finalizada",
        )
    if nuevo == actual:
        return False
    if actual == "confirmada" and nuevo == "cancelada":
        if ahora < inicio:
            return True
        raise ApiError(
            409,
            "TRANSICION_NO_PERMITIDA",
            "Transición no permitida",
            "Solo se puede cancelar una reserva confirmada cuando el horario de inicio todavía no llegó",
        )
    if actual == "confirmada" and nuevo == "finalizada":
        if ahora >= fin:
            return True
        raise ApiError(
            409,
            "TRANSICION_NO_PERMITIDA",
            "Transición no permitida",
            "Solo se puede finalizar una reserva confirmada cuando se alcanzó o superó el horario de finalización",
        )
    raise ApiError(
        409,
        "TRANSICION_NO_PERMITIDA",
        "Transición no permitida",
        f"No se puede pasar de {actual} a {nuevo}",
    )

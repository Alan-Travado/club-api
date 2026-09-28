from errors import ApiError
from reglas_horario import a_naive, validar_intervalo
from repositories import reservas as repo_reservas


def validador_reserva_nueva(id_cancha, id_socio, inicio, fin):
    """
    inicio y fin: datetime "aware" en GMT-3, ya parseados.
    Lanza ApiError si el intervalo no es válido o hay superposición.
    """
    validar_intervalo(inicio, fin)

    inicio_naive = a_naive(inicio)
    fin_naive = a_naive(fin)

    if repo_reservas.existe_superposicion_en_cancha(id_cancha, inicio_naive, fin_naive):
        raise ApiError(
            409,
            "CANCHA_NO_DISPONIBLE",
            "Esta cancha no está disponible",
            "Ya existe una reserva confirmada para esa cancha que se superpone con ese intervalo",
        )

    if repo_reservas.existe_superposicion_en_socio(id_socio, inicio_naive, fin_naive):
        raise ApiError(
            409,
            "SOCIO_NO_DISPONIBLE",
            "Socio no disponible",
            "El socio ya posee una reserva confirmada que se superpone con ese intervalo entonces no puede reservar otra cancha en ese horario",
        )

    if repo_reservas.existe_superposicion_en_bloqueo(
        id_cancha, inicio_naive.date(), inicio_naive.hour, fin_naive.hour
    ):
        raise ApiError(
            409,
            "CANCHA_NO_DISPONIBLE",
            "Está cancha no está disponible",
            "La cancha tiene un bloqueo por mantenimiento que se superpone con ese intervalo",
        )
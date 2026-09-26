from datetime import datetime, timedelta, timezone

from errors import ApiError

HORA_APERTURA = 8
HORA_CIERRE = 23
DURACION_MINIMA_HORAS = 1
DURACION_MAXIMA_HORAS = 3

# El club siempre trabajar en GMT-3
# esto sin importar que el servidor esté en otra zona horaria, o que el cliente esté en otra zona horaria.
ZONA_CLUB = timezone(timedelta(hours=-3))


def ahora():
    return datetime.now(ZONA_CLUB)


def a_naive(dt):
    """Quita el offset antes de guardar en MySQL, que no almacena zona horaria."""
    return dt.replace(tzinfo=None)


def _error(codigo, mensaje, detalle):
    return ApiError(400, codigo, mensaje, detalle)


def validar_intervalo(inicio, fin, limite_duracion=True):
    """
    inicio y fin deben ser datetime "aware" (con tzinfo), ya parseados.
    Lanza ApiError si el intervalo no cumple las reglas del club.
    Info pa los pibes : naive es un datetime sin zona horaria (no sabe si es UTC, Argentina, etc.), 
    y aware es un datetime que sí tiene esa información guardada en su atributo tzinfo.
    """
    if fin <= inicio:
        raise _error(
            "INTERVALO_INVALIDO",
            "Intervalo inválido",
            "fecha_hora_fin debe ser posterior a fecha_hora_inicio",
        )

    if inicio.microsecond or fin.microsecond or inicio.second or fin.second or \
            inicio.minute or fin.minute:
        raise _error(
            "HORA_INVALIDA",
            "Hora inválida",
            "Las reservas deben comenzar y terminar en una hora en punto",
        )

    if inicio.date() != fin.date():
        raise _error(
            "INTERVALO_INVALIDO",
            "Intervalo inválido",
            "La reserva no puede atravesar la medianoche",
        )

    if inicio.hour < HORA_APERTURA or fin.hour > HORA_CIERRE:
        raise _error(
            "FUERA_DE_HORARIO",
            "Fuera de horario",
            f"El club atiende de {HORA_APERTURA:02d}:00 a {HORA_CIERRE:02d}:00",
        )

    if limite_duracion:
        duracion_horas = (fin - inicio).total_seconds() / 3600
        if duracion_horas < DURACION_MINIMA_HORAS or duracion_horas > DURACION_MAXIMA_HORAS:
            raise _error(
                "DURACION_INVALIDA",
                "Duración inválida",
                f"Las reservas duran entre {DURACION_MINIMA_HORAS} y "
                f"{DURACION_MAXIMA_HORAS} horas completas",
            )

    if inicio <= ahora():
        raise _error(
            "FECHA_NO_FUTURA",
            "Fecha no futura",
            "El inicio de la reserva debe ser posterior al momento actual",
        )

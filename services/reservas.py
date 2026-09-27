import re

from errors import ApiError
from repositories import reservas as repo
from services.estado_reserva import ahora_gmt3, resolver_transicion
from services.canchas import obtener_cancha
from services.socios import obtener_socio
from services.disponibilidad import validador_reserva_nueva

def listar_reservas(filtros, limit, offset):
    return repo.listar(filtros, limit, offset)

def crear_reserva(datos):
    id_cancha = datos["id_cancha"]
    id_socio = datos["id_socio"]
    inicio = datos["fecha_hora_inicio"]
    fin = datos["fecha_hora_fin"]

    cancha = obtener_cancha(id_cancha)
    socio = obtener_socio(id_socio)

    if not cancha["activa"]:
        raise ApiError(
            409,
            "CANCHA_INACTIVA",
            "Cancha inactiva",
            "La cancha no admite nuevas reservas",
        )

    if not socio["activo"]:
        raise ApiError(
            409,
            "SOCIO_INACTIVO",
            "Socio inactivo",
            "El socio no puede realizar nuevas reservas",
        )

    validador_reserva_nueva(
        id_cancha,
        id_socio,
        inicio,
        fin,
    )

    duracion_horas = int((fin - inicio).total_seconds() / 3600)
    precio_hora = cancha["precio_hora"]

    reserva = {
        "id_socio": id_socio,
        "id_cancha": id_cancha,
        "fecha_hora_inicio": inicio,
        "fecha_hora_fin": fin,
        "estado": "confirmada",
        "precio_hora": precio_hora,
        "precio_total": precio_hora * duracion_horas,
    }

    return repo.crear(reserva)

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

def obtener_reserva(id_reserva):
    reserva = repo.obtener_por_id(id_reserva)

    if reserva is None:
        raise ApiError(
            404,
            "RESERVA_NO_ENCONTRADA",
            "Reserva no encontrada",
            f"No existe una reserva con id {id_reserva}"
        )
    return repo.formatear(reserva)

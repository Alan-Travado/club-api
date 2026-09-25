from datetime import timedelta
from errors import ApiError
from services.disponibilidad import validador_reserva_nueva as validar_reserva_nueva
from services.canchas import obtener_cancha
from services.socios import obtener_socio

def validar_recursos(id_cancha, id_socio):
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
    return cancha, socio

def generar_serie(inicio, fin, cantidad_semanas):
    reservas = []

    for semana in range(cantidad_semanas):
        desplazamiento = timedelta(weeks=semana)
        reservas.append({
            "fecha_hora_inicio": inicio + desplazamiento,
            "fecha_hora_fin": fin + desplazamiento
        })
    return reservas

def detectar_conflictos(id_cancha, id_socio, serie):
    conflictos = []

    for reserva in serie:
        inicio = reserva["fecha_hora_inicio"]
        fin = reserva["fecha_hora_fin"]

        try:
            validar_reserva_nueva(
                id_cancha,
                id_socio,
                inicio,
                fin
            )
        except ApiError as error:
            if error.status == 409:
                conflictos.append(inicio.date().isoformat())
            else:
                raise
    return conflictos

def preparar_serie(datos):
    id_cancha = datos["id_cancha"]
    id_socio = datos["id_socio"]

    cancha, socio = validar_recursos(id_cancha, id_socio)
    serie = generar_serie(
        datos["fecha_hora_inicio"],
        datos["fecha_hora_fin"],
        datos["cantidad_semanas"]
    )
    conflictos = detectar_conflictos(id_cancha, id_socio, serie)

    if conflictos:
        raise ApiError(
            409,
            "RESERVAS_NO_DISPONIBLES",
            "Conflicto en la serie de reservas",
            "Una o más fechas no están disponibles",
            conflictos=conflictos,
        )
    return cancha, socio, serie

def completar_reservas(cancha, socio, serie):
    reservas = []
    precio_hora = cancha["precio_hora"]

    for reserva in serie:
        inicio = reserva["fecha_hora_inicio"]
        fin = reserva["fecha_hora_fin"]
        duracion_horas = int((fin - inicio).total_seconds() / 3600)

        reservas.append({
            "id_cancha": cancha["id"],
            "id_socio": socio["id"],
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin,
            "estado": "confirmada",
            "precio_hora": precio_hora,
            "precio_total": precio_hora * duracion_horas,
        })
    return reservas
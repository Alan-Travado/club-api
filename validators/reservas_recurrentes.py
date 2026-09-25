import re
from datetime import datetime, timedelta

from validators.comunes import (
    campo_entero_positivo,
    error_campo,
    validar_cuerpo,
)

PATRON_FECHA_HORA = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}-03:00$"
)

CAMPOS_CREATE = {
    "id_socio",
    "id_cancha",
    "fecha_hora_inicio",
    "fecha_hora_fin",
    "cantidad_semanas",
}

def campo_fecha_hora(body, nombre):
    valor = body.get(nombre)

    if not isinstance(valor, str):
        raise error_campo(
            nombre,
            "debe ser una fecha y hora válida"
        )
    
    if not PATRON_FECHA_HORA.fullmatch(valor):
        raise error_campo(
            nombre,
            "debe tener un formato YYYY-MM-DDTHH:MM:SS.ffffff-03:00"
        )

    try:
        fecha = datetime.fromisoformat(valor)
    except ValueError:
        raise error_campo(nombre, "debe tener un formato de fecha y hora válido")

    if fecha.utcoffset() != timedelta(hours=-3):
        raise error_campo(nombre, "debe estar en la zona horaria UTC-3")

    return fecha
    
def validar_creacion(body):
    validar_cuerpo(body, CAMPOS_CREATE)

    id_socio = campo_entero_positivo(
        body, "id_socio", requerido=True
    )

    id_cancha = campo_entero_positivo(
        body, "id_cancha", requerido=True
    )

    cantidad_semanas = campo_entero_positivo(
        body, "cantidad_semanas", requerido=True
    )

    if cantidad_semanas > 12:
        raise error_campo(
            "cantidad_semanas",
            "debe estar entre 2 y 12"
        )

    if cantidad_semanas < 2:
        raise error_campo(
            "cantidad_semanas",
            "debe estar entre 2 y 12"
        )

    inicio = campo_fecha_hora(body, "fecha_hora_inicio")
    fin = campo_fecha_hora(body, "fecha_hora_fin")

    if fin <= inicio:
        raise error_campo(
            "fecha_hora_fin",
            "debe ser posterior a fecha_hora_inicio"
        )

    return {
        "id_socio": id_socio,
        "id_cancha": id_cancha,
        "fecha_hora_inicio": inicio,
        "fecha_hora_fin": fin,
        "cantidad_semanas": cantidad_semanas,
    }
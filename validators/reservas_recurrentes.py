from validators.comunes import (
    campo_entero_positivo,
    campo_fecha_hora,
    error_campo,
    validar_cuerpo,
)

CAMPOS_CREATE = {
    "id_socio",
    "id_cancha",
    "fecha_hora_inicio",
    "fecha_hora_fin",
    "cantidad_semanas",
}

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

    inicio = campo_fecha_hora(
        body, "fecha_hora_inicio", requerido=True
    )
    fin = campo_fecha_hora(
        body, "fecha_hora_fin", requerido=True
    )

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
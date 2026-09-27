from datetime import datetime

from errors import ApiError
from validators.comunes import (
    campo_fecha_hora,
    entero,
    error_campo,
    error_parametro,
    leer_paginacion,
    validar_cuerpo,
    validar_parametros_permitidos,
    campo_entero_positivo,
)

PARAMS_LISTADO = {
    "id_cancha",
    "id_socio",
    "estado",
    "fecha_desde",
    "fecha_hasta",
    "_limit",
    "_offset",
}
ESTADOS = {"confirmada", "cancelada", "finalizada"}
CAMPOS_CREATE = {"id_socio", "id_cancha", "fecha_hora_inicio", "fecha_hora_fin"}


def validar_filtros_listado(args):
    validar_parametros_permitidos(args, PARAMS_LISTADO)
    limit, offset = leer_paginacion(args)
    filtros = {
        "id_cancha": None,
        "id_socio": None,
        "estado": None,
        "fecha_desde": None,
        "fecha_hasta": None,
    }
    if "id_cancha" in args:
        filtros["id_cancha"] = entero(args["id_cancha"], "id_cancha", 1)
    if "id_socio" in args:
        filtros["id_socio"] = entero(args["id_socio"], "id_socio", 1)
    if "estado" in args:
        if args["estado"] not in ESTADOS:
            raise error_parametro("estado", "debe ser confirmada, cancelada o finalizada")
        filtros["estado"] = args["estado"]
    if "fecha_desde" in args:
        filtros["fecha_desde"] = _fecha(args["fecha_desde"], "fecha_desde")
    if "fecha_hasta" in args:
        filtros["fecha_hasta"] = _fecha(args["fecha_hasta"], "fecha_hasta")
    if (
        filtros["fecha_desde"] is not None
        and filtros["fecha_hasta"] is not None
        and filtros["fecha_desde"] > filtros["fecha_hasta"]
    ):
        raise error_parametro("fecha_desde", "debe ser anterior o igual a fecha_hasta")
    return filtros, limit, offset


def validar_cambio_estado(body):
    validar_cuerpo(body, {"estado"})
    if "estado" not in body:
        raise error_campo("estado", "es obligatorio")
    estado = body["estado"]
    if not isinstance(estado, str) or estado not in ESTADOS:
        raise error_campo("estado", "debe ser confirmada, cancelada o finalizada")
    return estado


def validar_id(id_reserva):
    if id_reserva < 1:
        raise ApiError(
            400,
            "PARAMETRO_INVALIDO",
            "Parámetro inválido",
            "El id debe ser un entero positivo",
        )


def _fecha(valor, nombre):
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError:
        raise error_parametro(nombre, "debe ser una fecha con formato YYYY-MM-DD")

def validar_creacion(body):
    validar_cuerpo(body, CAMPOS_CREATE)

    return {
        "id_socio": campo_entero_positivo(
            body,
            "id_socio",
            requerido=True,
        ),
        "id_cancha": campo_entero_positivo(
            body,
            "id_cancha",
            requerido=True,
        ),
        "fecha_hora_inicio": campo_fecha_hora(
            body,
            "fecha_hora_inicio",
            requerido=True,
        ),
        "fecha_hora_fin": campo_fecha_hora(
            body,
            "fecha_hora_fin",
            requerido=True
        ),
    }

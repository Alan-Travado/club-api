from errors import ApiError


def error_parametro(nombre, detalle):
    return ApiError(
        400,
        "PARAMETRO_INVALIDO",
        "Parámetro inválido",
        f"El parámetro '{nombre}' {detalle}",
    )


def error_campo(nombre, detalle):
    return ApiError(
        400,
        "CAMPO_INVALIDO",
        "Campo inválido",
        f"El campo '{nombre}' {detalle}",
    )


def validar_parametros_permitidos(args, permitidos):
    desconocidos = sorted(set(args.keys()) - set(permitidos))
    if desconocidos:
        raise ApiError(
            400,
            "PARAMETRO_DESCONOCIDO",
            "Parámetro desconocido",
            f"Parámetros no admitidos: {', '.join(desconocidos)}",
        )


def validar_cuerpo(body, permitidos):
    if not isinstance(body, dict) or not body:
        raise ApiError(
            400,
            "CUERPO_INVALIDO",
            "Cuerpo inválido",
            "El cuerpo de la solicitud debe ser un objeto JSON no vacío",
        )
    desconocidos = sorted(set(body.keys()) - set(permitidos))
    if desconocidos:
        raise ApiError(
            400,
            "CAMPO_DESCONOCIDO",
            "Campo desconocido",
            f"Campos no admitidos: {', '.join(desconocidos)}",
        )


def entero(valor, nombre, minimo, maximo=None):
    if not (valor.isascii() and valor.isdigit()):
        raise error_parametro(nombre, "debe ser un número entero")
    numero = int(valor)
    if numero < minimo:
        raise error_parametro(nombre, f"debe ser mayor o igual a {minimo}")
    if maximo is not None and numero > maximo:
        raise error_parametro(nombre, f"debe ser menor o igual a {maximo}")
    return numero


def booleano(valor, nombre):
    if valor == "true":
        return True
    if valor == "false":
        return False
    raise error_parametro(nombre, "debe ser true o false")


def texto_no_vacio(valor, nombre):
    limpio = valor.strip()
    if not limpio:
        raise error_parametro(nombre, "no puede estar vacío")
    return limpio


def leer_paginacion(args):
    limit = entero(args["_limit"], "_limit", 1, 100) if "_limit" in args else 10
    offset = entero(args["_offset"], "_offset", 0) if "_offset" in args else 0
    return limit, offset


def campo_texto_no_vacio(body, nombre, requerido, actual=None):
    if nombre not in body:
        if requerido:
            raise error_campo(nombre, "es obligatorio")
        return actual
    valor = body[nombre]
    if not isinstance(valor, str):
        raise error_campo(nombre, "debe ser un texto")
    limpio = valor.strip()
    if not limpio:
        raise error_campo(nombre, "no puede quedar vacío")
    return limpio


def campo_entero_positivo(body, nombre, requerido, actual=None):
    if nombre not in body:
        if requerido:
            raise error_campo(nombre, "es obligatorio")
        return actual
    valor = body[nombre]
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise error_campo(nombre, "debe ser un entero")
    if valor <= 0:
        raise error_campo(nombre, "debe ser mayor a cero")
    return valor


def campo_booleano(body, nombre, actual):
    if nombre not in body:
        return actual
    valor = body[nombre]
    if not isinstance(valor, bool):
        raise error_campo(nombre, "debe ser true o false")
    return valor


import re
from datetime import datetime, date, time, timedelta

from reglas_horario import ZONA_CLUB

_PATRON_FECHA_HORA = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}-03:00$"
)
_PATRON_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_PATRON_HORA = re.compile(r"^([01]\d|2[0-3]):00:00$")

def fechas_a_texto(fila):
    for clave, valor in fila.items():
        if isinstance(valor, (date, time, timedelta)):
            fila[clave] = str(valor)
    return fila

def campo_fecha_hora(body, nombre, requerido, actual=None):
    if nombre not in body:
        if requerido:
            raise error_campo(nombre, "es obligatorio")
        return actual
    valor = body[nombre]
    if not isinstance(valor, str) or not _PATRON_FECHA_HORA.match(valor):
        raise error_campo(
            nombre,
            "debe tener el formato YYYY-MM-DDTHH:MM:SS.ffffff-03:00",
        )
    try:
        return datetime.strptime(valor, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError as exc:
        raise error_campo(nombre, "no es una fecha válida") from exc

def campo_fecha(body, nombre):
    if nombre not in body:
        raise error_campo(nombre, 'es obligatorio')
    valor = body[nombre]
    if not isinstance(valor, str):
        raise error_campo(nombre, 'debe ser un texto con formato YYYY-MM-DD')
    try:
        return parametro_fecha(valor, nombre)
    except Exception:
        raise error_campo(nombre, 'debe tener el formato YYYY-MM-DD')

def campo_hora(body, nombre):
    if nombre not in body:
        raise error_campo(nombre, 'es obligatorio')
    valor = body[nombre]
    if not isinstance(valor, str):
        raise error_campo(nombre, 'debe ser un texto con formato HH:00:00')
    try:
        return parametro_hora(valor, nombre)
    except Exception:
        raise error_campo(nombre, 'debe tener el formato HH:00:00 (hora en punto)')

def parametro_fecha(valor, nombre):
    if not _PATRON_FECHA.match(valor):
        raise error_parametro(nombre, "el patron de la fecha debe ser YYYY-MM-DD")
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError as exc:
        raise error_parametro(nombre, "no es una fecha válida") from exc


def parametro_hora(valor, nombre):
    if not _PATRON_HORA.match(valor):
        raise error_parametro(nombre, "el patron de la hora debe ser HH:00:00 (hora en punto)")
    return int(valor[:2])


def combinar_fecha_hora(fecha, hora):
    return datetime(fecha.year, fecha.month, fecha.day, hora, tzinfo=ZONA_CLUB)

from validators.comunes import (
    booleano,
    campo_booleano,
    campo_texto_no_vacio,
    error_campo,
    leer_paginacion,
    texto_no_vacio,
    validar_cuerpo,
    validar_parametros_permitidos,
    normalizar_y_validar_email,
)

PARAMS_LISTADO = {"nombre", "activo", "_limit", "_offset"}
CAMPOS_CREATE = {"nombre", "email"}
CAMPOS_UPDATE = {"nombre", "email", "activo"}


def validar_filtros_listado(args):
    validar_parametros_permitidos(args, PARAMS_LISTADO)
    limit, offset = leer_paginacion(args)

    filtros = {
        "nombre": None,
        "activo": None,
    }
    if "nombre" in args:
        filtros["nombre"] = texto_no_vacio(args["nombre"], "nombre")
    if "activo" in args:
        filtros["activo"] = booleano(args["activo"], "activo")

    return filtros, limit, offset


def campo_email(body, nombre, requerido, actual=None):
    if nombre not in body:
        if requerido:
            raise error_campo(nombre, "es obligatorio")
        return actual

    return normalizar_y_validar_email(body[nombre])


def validar_creacion(body):
    validar_cuerpo(body, CAMPOS_CREATE)

    return {
        "nombre": campo_texto_no_vacio(body, "nombre", requerido=True),
        "email": campo_email(body, "email", requerido=True),
        "activo": True,
    }


def validar_actualizacion(body, actual):
    validar_cuerpo(body, CAMPOS_UPDATE)

    return {
        "nombre": campo_texto_no_vacio(
            body, "nombre", requerido=False, actual=actual["nombre"]
        ),
        "email": campo_email(body, "email", requerido=False, actual=actual["email"]),
        "activo": campo_booleano(body, "activo", actual=actual["activo"]),
    }

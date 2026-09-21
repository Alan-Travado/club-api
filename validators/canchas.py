from validators.comunes import (
    booleano,
    entero,
    leer_paginacion,
    texto_no_vacio,
    validar_parametros_permitidos,
)

PARAMS_LISTADO = {"id_deporte", "nombre", "techada", "activa", "_limit", "_offset"}


def validar_filtros_listado(args):
    validar_parametros_permitidos(args, PARAMS_LISTADO)
    limit, offset = leer_paginacion(args)

    filtros = {
        "id_deporte": None,
        "nombre": None,
        "techada": None,
        "activa": None,
    }
    if "id_deporte" in args:
        filtros["id_deporte"] = entero(args["id_deporte"], "id_deporte", 1)
    if "nombre" in args:
        filtros["nombre"] = texto_no_vacio(args["nombre"], "nombre")
    if "techada" in args:
        filtros["techada"] = booleano(args["techada"], "techada")
    if "activa" in args:
        filtros["activa"] = booleano(args["activa"], "activa")

    return filtros, limit, offset

from errors import ApiError
from repositories import deportes as repo_deportes
from validators.comunes import (
    booleano,
    campo_booleano,
    campo_entero_positivo,
    campo_texto_no_vacio,
    entero,
    leer_paginacion,
    texto_no_vacio,
    validar_cuerpo,
    validar_parametros_permitidos,
    parametro_fecha,
    parametro_hora,
    combinar_fecha_hora,
)

PARAMS_LISTADO = {"id_deporte", "nombre", "techada", "activa", "_limit", "_offset"}
PARAMS_DISPONIBILIDAD = {"fecha", "hora_inicio", "hora_fin", "id_deporte", "tachada", "_limit", "_offset"}
CAMPOS_CREATE = {"nombre", "id_deporte", "precio_hora", "techada", "activa"}
CAMPOS_UPDATE = {"nombre", "precio_hora", "techada", "activa"}


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


def _validar_deporte_existente(id_deporte):
    if not repo_deportes.existe(id_deporte):
        raise ApiError(
            404,
            "DEPORTE_NO_ENCONTRADO",
            "Deporte no encontrado",
            f"No existe un deporte con id {id_deporte}",
        )


def validar_creacion(body):
    validar_cuerpo(body, CAMPOS_CREATE)

    nombre = campo_texto_no_vacio(body, "nombre", requerido=True)
    id_deporte = campo_entero_positivo(body, "id_deporte", requerido=True)
    precio_hora = campo_entero_positivo(body, "precio_hora", requerido=True)
    techada = campo_booleano(body, "techada", actual=False)
    activa = campo_booleano(body, "activa", actual=True)

    _validar_deporte_existente(id_deporte)

    return {
        "nombre": nombre,
        "id_deporte": id_deporte,
        "precio_hora": precio_hora,
        "techada": techada,
        "activa": activa,
    }

def validar_actualizacion(body):
    validar_cuerpo(body, CAMPOS_UPDATE)

    datos = {}

    if "nombre" in body:
        datos["nombre"] = campo_texto_no_vacio(
            body,
            "nombre",
            requerido=False,
        )

    if "precio_hora" in body:
        datos["precio_hora"] = campo_entero_positivo(
            body,
            "precio_hora",
            requerido=False,
        )

    if "techada" in body:
        datos["techada"] = campo_booleano(
            body,
            "techada",
            actual=None,
        )

    if "activa" in body:
        datos["activa"] = campo_booleano(
            body,
            "activa",
            actual=None,
        )

    return datos

def validar_disponibilidad(args):
    validar_parametros_permitidos(args, PARAMS_DISPONIBILIDAD)

    if "fecha" not in args:
        raise ApiError(
            400,
            "PARAMETRO_FALTANTE",
            "Parámetro faltante",
            "El parámetro 'fecha' es obligatorio",
        )

    if "hora_inicio" not in args:
        raise ApiError(
            400,
            "PARAMETRO_FALTANTE",
            "Parámetro faltante",
            "El parámetro 'hora_inicio' es obligatorio",
        )

    if "hora_fin" not in args:
        raise ApiError(
            400,
            "PARAMETRO_FALTANTE",
            "Parámetro faltante",
            "El parámetro 'hora_fin' es obligatorio",
        )

    fecha = parametro_fecha(args["fecha"], "fecha")
    hora_inicio = parametro_hora(args["hora_inicio"], "hora_inicio")
    hora_fin = parametro_hora(args["hora_fin"], "hora_fin")

    inicio = combinar_fecha_hora(fecha, hora_inicio)
    fin = combinar_fecha_hora(fecha, hora_fin)

    filtros = {
        "id_deporte": None,
        "techada": None,
    }

    if "id_deporte" in args:
        filtros["id_deporte"] = entero(
            args["id_deporte"],
            "id_deporte",
            1,
        )

    if "techada" in args:
        filtros["techada"] = booleano(
            args["techada"],
            "techada",
        )

    limit, offset = leer_paginacion(args)

    return filtros, inicio, fin, limit, offset
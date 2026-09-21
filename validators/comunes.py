from errors import ApiError


def error_parametro(nombre, detalle):
    return ApiError(
        400,
        "PARAMETRO_INVALIDO",
        "Parámetro inválido",
        f"El parámetro '{nombre}' {detalle}",
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

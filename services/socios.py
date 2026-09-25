from errors import ApiError
from repositories import socios as repo


def _error_email_duplicado(email):
    return ApiError(
        409,
        "EMAIL_DUPLICADO",
        "Email ya registrado",
        f"Ya existe un socio con el email '{email}'",
    )


def obtener_socio(id_socio):
    socio = repo.obtener_por_id(id_socio)
    if socio is None:
        raise ApiError(
            404,
            "SOCIO_NO_ENCONTRADO",
            "Socio no encontrado",
            f"No existe un socio con id {id_socio}",
        )
    return socio


def listar_socios(filtros, limit, offset):
    return repo.listar(filtros, limit, offset)


def crear_socio(datos):
    if repo.obtener_por_email(datos["email"]) is not None:
        raise _error_email_duplicado(datos["email"])
    return repo.crear(datos)


def actualizar_socio(id_socio, datos):
    obtener_socio(id_socio)
    if repo.obtener_por_email(datos["email"], excluir_id=id_socio) is not None:
        raise _error_email_duplicado(datos["email"])
    return repo.actualizar(id_socio, datos)

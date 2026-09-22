from errors import ApiError
from repositories import canchas as repo


def obtener_cancha(id_cancha):
    cancha = repo.obtener_por_id(id_cancha)
    if cancha is None:
        raise ApiError(
            404,
            "CANCHA_NO_ENCONTRADA",
            "Cancha no encontrada",
            f"No existe una cancha con id {id_cancha}",
        )
    return cancha


def listar_canchas(filtros, limit, offset):
    return repo.listar(filtros, limit, offset)


def crear_cancha(datos):
    return repo.crear(datos)

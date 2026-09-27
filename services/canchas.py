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

def actualizar_cancha(id_cancha, datos):
    obtener_cancha(id_cancha)
    return repo.actualizar(id_cancha, datos)


def eliminar_cancha(id_cancha):
    obtener_cancha(id_cancha)

    if repo.contar_reservas(id_cancha) > 0:
        raise ApiError(
            409,
            "CANCHA_CON_RESERVAS",
            "No se puede eliminar la cancha",
            f"La cancha con id {id_cancha} tiene reservas asociadas",
        )

    repo.eliminar(id_cancha)
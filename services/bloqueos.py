from errors import ApiError
from repositories import bloqueos as repo

def listar_bloqueos(filtros, limit, offset):
    return repo.listar(filtros, limit, offset)

def crear_bloqueo(datos):
    id_cancha = datos["id_cancha"]
    fecha = datos["fecha"]
    hora_inicio = datos["hora_inicio"]
    hora_fin = datos["hora_fin"]

    if not repo.existe_cancha(id_cancha):
        raise ApiError(
            404,
            "CANCHA_NO_ENCONTRADA",
            "Cancha no encontrada",
            f"No existe una cancha con id {id_cancha}",
        )
    if repo.hay_superposicion_con_bloqueo(datos):
        raise ApiError(
            409,
            "BLOQUEO_SUPERPUESTO",
            "Bloqueos superpuestos",
            "Ya existe un bloqueo para esa cancha que se superpone con ese horario",
        )
    if repo.hay_superposicion_con_reserva(id_cancha, fecha, hora_inicio, hora_fin):
        raise ApiError(
            409,
            "RESERVA_SUPERPUESTA",
            "Reserva confirmada en ese horario",
            "Existe una reserva confirmada para esa cancha que se superpone con ese horario",
        )
    return repo.crear(datos)

def eliminar_bloqueo(id_bloqueo):
    if not repo.eliminar(id_bloqueo):
        raise ApiError(
            404,
            "BLOQUEO_NO_ENCONTRADO",
            "Bloqueo no encontrado",
            f"No existe un bloqueo con el id {id_bloqueo}",
        )
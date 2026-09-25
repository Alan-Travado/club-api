from errors import ApiError
from repositories import bloqueos as repo

def listar_bloqueos(filtros, limit, offset):
    return repo.listar(filtros, limit, offset)

def crear_bloqueo(datos):
    if not repo.existe_cancha(datos['id_cancha']):
        raise ApiError(
            404,
            'CANCHA_NO_ENCONTRADA',
            'Cancha no encontrada',
            f'No existe una cancha con id {datos['id_cancha']}',
        )
    if repo.hay_superposicion(datos):
        raise ApiError(
            409,
            'BLOQUE_SUPERPUESTO',
            'Bloqueos superpuestos',
            'Ya existe un bloqueo para esa cancha en ese horario o parecido a el mismo',
        )
    return repo.crear(datos)

def eliminar_bloqueo(id_bloqueo):
    if not repo.eliminar(id_bloqueo):
        raise ApiError(
            404,
            'BLOQUEO_NO_ENCONTRADO',
            'Bloqueo no encontrado',
            f'No existe un bloqueo con el id {id_bloqueo}',
        )